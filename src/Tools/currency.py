from enum import Enum
from typing import Optional
import json

from langchain.tools import BaseTool

from pydantic import Field, BaseModel
from dotenv import load_dotenv
from datetime import datetime
import requests
import os, getpass
import pandas as pd

from src.utils import check_shrink_df
from src.constants import request_date

class CurrencyEnum(str, Enum):
    EUR = "EUR"
    USD = "USD"
    TRY = "TRY"

class CurrencyToolInput(BaseModel):
    action: str = Field(description="The action to perform, either 'get_currency_data' or 'merge_currencies'.")
    base_currency: CurrencyEnum = Field(description="The base currency to use for conversions. Required for both 'get_currency_data' and 'merge_currencies'.")
    currency_column: Optional[str] = Field(default=None, description="The name of the column containing currency codes. Required for 'merge_currencies'.")
    money_columns: Optional[list[str]] = Field(default=None, description="A list of column names containing monetary values to be converted. Required for 'merge_currencies'.")

class CurrencyTool(BaseTool):
    args_schema = CurrencyToolInput
    name: str = "currency_tool"
    description: str = """A tool for currency conversion and merging.
    
    Actions:
    - 'get_currency_data': Fetches currency exchange rates. Requires 'base_currency'.
    - 'merge_currencies': Merges currencies in a DataFrame. Requires 'base_currency', 'currency_column', and 'money_columns' and 'row_count'.
    
    Before merging, you must first run 'get_currency_data' to fetch the necessary exchange rates.
    """
    base_currency: Optional[CurrencyEnum] = Field(default=None, description="The main currency which others will be merged into")
    df: Optional[pd.DataFrame] = Field(default=None, description="The dataframe which's currencies will be merged")
    api_data: Optional[dict] = Field(default=None, description="The api data that is fetched with get_currency_data")
    last_request: Optional[datetime] = Field(default=None, description="The last time currency data was requested")

    def _run(self, action: str, base_currency: CurrencyEnum, currency_column: Optional[str] = None, money_columns: Optional[list[str]] = None):
        """Main execution method required by BaseTool."""
        print("CurrencyTool: Running...")
        try:
            print("CurrencyTool: Loading last request...")
            self.load_last_request(filepath=request_date)
            print("CurrencyTool: Last request loaded...")

            if action == "get_currency_data":
                if self.check_last_request() and self.api_data:
                    return self.api_data
                data = self._get_currency_data(base_currency)
                if data and isinstance(data, requests.Response):
                    self.api_data = data.json()
                    self.write_last_request(filepath=request_date, data=self.api_data)
                    return self.api_data
                elif isinstance(data, dict):
                    self.api_data = data
                    self.write_last_request(filepath=request_date, data=self.api_data)
                    return self.api_data
                else:
                    return data
            
            elif action == "merge_currencies":
                self.base_currency = base_currency
                if self.api_data is None:
                    # If api_data is not available, fetch it first
                    print("Currency data not found, fetching...")
                    data = self._get_currency_data(base_currency)
                    if data and isinstance(data, requests.Response):
                        self.api_data = data.json()
                        self.write_last_request(filepath=request_date, data=self.api_data)
                    elif isinstance(data, dict):
                        self.api_data = data
                        self.write_last_request(filepath=request_date, data=self.api_data)
                    else:
                        return data # Return error from fetch

                if not currency_column or not money_columns:
                    return "Missing required parameters: currency_column and/or money_columns."
                if self.df is None:
                    return "No DataFrame available. Please provide a DataFrame."
                
                result_df = self._merge_currencies(
                    self.api_data, 
                    currency_column, 
                    money_columns
                )
                result_df, info = check_shrink_df(result_df, 10)
                return result_df

            else:
                return f"Unknown action: {action}"
        except Exception as e:
            print(f"CurrencyTool: Error: {e}")
            return f"Error processing input: {str(e)}"

    def load_last_request(self, filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
            value = data.get("currency_api")
            if isinstance(value, str):
                self.last_request = datetime.fromisoformat(value)
            else:
                self.last_request = None
            base_currency_str = data.get("base_currency")
            if base_currency_str:
                self.base_currency = CurrencyEnum(base_currency_str)
            else:
                self.base_currency = None
            self.api_data = data.get("data")
    
    def write_last_request(self, filepath, data=None):
        """
        Write the last request date and optional data to the given file as JSON, with indent=2 for readability.
        """
        payload = {
            "currency_api": self.last_request.isoformat() if self.last_request else None,
            "base_currency": self.base_currency.value if self.base_currency else None,
            "data": data if data is not None else {}
        }
        with open(filepath, "w") as f:
            json.dump(payload, f, indent=2)

    def check_last_request(self):
        """
        Check if the last request was made today. Returns False if last_request is not set.
        """
        print("CurrencyTool: Checking last request...")
        if not hasattr(self, 'last_request') or self.last_request is None:
            return True  # Allow if never requested
        return self.last_request.date() == datetime.today().date()

    def _get_currency_data(self, base_currency):
        """
        Get the relative currency rates from the base_currency's perspective
        """
        print("Fetching currency rates (may take a few seconds)...")
        load_dotenv()
        # Ensure base_currency is a CurrencyEnum
        if isinstance(base_currency, str):
            base_currency = CurrencyEnum(base_currency)
        self.base_currency = base_currency
        try:
            api_key = os.getenv('FREE_CURRENCY_API_KEY')
            if not api_key:
                api_key = getpass.getpass("Please enter your api key for freecurrencyapi")

            currencies = "%2C".join([e.value for e in CurrencyEnum])

            url = (
                f"https://api.freecurrencyapi.com/v1/latest"
                f"?apikey={api_key}&currencies={currencies}&base_currency={self.base_currency.value}"
            )

            response = requests.get(url=url)
            if response.status_code != 200:
                return f"API error: {response.status_code} - {response.text}"
            self.last_request = datetime.today()
            return response

        except Exception as e:
            print(f"CurrencyTool: Error initializing currency api: {e}")
            return f"Error initializing currency api: {e}"

    def _merge_currencies(self, api_data, currency_column, money_columns):
        """
        Adds a 'rate' column to the DataFrame by mapping currency codes to rates,
        and converts all specified money columns to the base currency.
        Parameters:
            api_data: dict, API response with rates under 'data'
            currency_column: str or list, name(s) of the column(s) in self.df with currency codes
            money_columns: list of str, columns to convert to base currency
        """
        print("CurrencyTool: Merging currencies...")
        if self.df is None:
            return "DataFrame is not set."
        if api_data is None or "data" not in api_data:
            return "API data is missing or invalid."
        rates = api_data["data"]
        # Support both string and list for currency_column
        if isinstance(currency_column, list):
            for col in currency_column:
                self.df["rate"] = self.df[col].map(rates)
        else:
            self.df["rate"] = self.df[currency_column].map(rates)
        if not isinstance(money_columns, list):
            money_columns = [money_columns]
        for col in money_columns:
            self.df[f"{col}_in_{self.base_currency.value if self.base_currency else 'BASE'}"] = self.df[col] * self.df["rate"]
        return self.df