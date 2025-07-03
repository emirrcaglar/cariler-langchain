from enum import Enum
from typing import Optional
from langchain.tools import BaseTool
from pydantic import Field
from dotenv import load_dotenv
import requests
import os, getpass
import pandas as pd
from datetime import datetime
from src.constants import request_date

class CurrencyEnum(str, Enum):
    EUR = "EUR"
    USD = "USD"
    TRY = "TRY"

class CurrencyTool(BaseTool):
    name = "currency_tool"
    description: str = """Converts currencies, merges them into selected one. 
    Input should be a JSON string with two keys: 
    'action' ('get_currency_data' or 'merge_currencies'), 
    and 'params' (dictionary with 'base_currency', ).
    'group_by' should be a list of column names to group by,
    aggregation should be a string like "min", "sum", etc.)"""
    base_currency: CurrencyEnum = Field(..., description="The main currency which others will be merged into")
    df: pd.DataFrame = Field(..., description="The dataframe which's currencies will be merged")
    api_data: Optional[dict] = Field(..., description="The api data that is fetched with get_currency_data")
    last_request: datetime

    def _run(self, tool_input):
        """Main execution method required by BaseTool"""
        try:
            self.load_last_request(filepath=request_date)
            import json
            data = json.loads(tool_input)
            action = data['action']
            params = data['params']

            if action == "get_currency_data":
                if not self.check_last_request():
                    return 
                base_currency = params['base_currency']
                data = self._get_currency_data(base_currency)
                if data and isinstance(data, requests.Response):
                    self.api_data = data.json()
                elif isinstance(data, dict):
                    self.api_data = data
                else:
                    return data
            elif action == "merge_currencies":
                self._merge_currencies(
                    self.api_data, 
                    params['currency_columns'], 
                    params['money_columns']
                    )
        except Exception as e:
            return f"Error initializing CurrencyTool: {e}"   

    def load_last_request(self, filepath):
        import json
        with open(filepath, "r") as f:
            data = json.load(f)
            self.last_request = datetime.fromisoformat(data["currency_api"])
    
    def write_last_request(self, filepath, data):
        import json
        with open(filepath, "w") as f:
            f.write({
                "currency_api": datetime.today().date(),
                "data": 
            })

    def _get_currency_data(self, base_currency: CurrencyEnum):
        """
        Get the relative currency rates from the base_currency's perspective
        """
        load_dotenv()
        
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
            print(f"Error initializing currency api: {e}")
            return f"Error initializing currency api: {e}"

    # Example API response:
    # {
    #   "data": {
    #     "EUR": 0.8472401461,
    #     "TRY": 39.911076514,
    #     "USD": 1
    #   }
    # } 

    def _merge_currencies(self, api_data, currency_column, money_columns):
        """
        Adds a 'rate' column to the DataFrame by mapping currency codes to rates,
        and converts all specified money columns to the base currency.
        
        Parameters:
            api_data: dict, API response with rates under 'data'
            currency_column: str, name of the column in self.df with currency codes
            money_columns: list of str, columns to convert to base currency
        """
        api_data = self.api_data
        if api_data:
            rates = api_data["data"]
            self.df["rate"] = self.df[currency_column].map(rates)

            for col in money_columns:
                self.df[f"{col}_in_{self.base_currency.value}"] = self.df[col] * self.df["rate"]
            return self.df

    def check_last_request(self):
        return self.last_request.date() == datetime.today().date()
    

    
