import pandas as pd
import re
from pydantic import Field, PrivateAttr
from langchain.tools import BaseTool

from src.utils import check_shrink_df
from src.constants import MAX_ROWS


class DataFrameFilterTool(BaseTool):
    name: str = "dataframe_transformer"
    description: str = """Useful for transforming and filtering DataFrame data. 
    Input should be a JSON string with two keys: 
    'action' ('filter_data'), 
    and 'params' ('columns' for select_columns, 'condition' for filter_data).
    Prioritize filtering with the `contains()` function.
    DO NOT use direct equality checks for floating-point numbers due to precision issues.
    For example, instead of `Col == 123.45`, use `Col >= 123.45 and Col < 123.46`."""

    df: pd.DataFrame = Field(..., description="The pandas DataFrame to filter")
    _original_df: pd.DataFrame = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._original_df = self.df.copy()

    def _run(self, tool_input: str) -> str:
        """Main execution method required by BaseTool"""
        try:
            import json
            data = json.loads(tool_input)
            action = data['action']
            params = data['params']

            if action == "filter_data":
                return self._filter_data(params['condition'].strip())
            return "Invalid action. Use either 'group_by' or 'apply_aggregation'"
        except Exception as e:
            error_message = f"Error processing input: {str(e)}"
            return error_message

    def _filter_data(self, condition: str):
        """
        Standardize and filter the data.
        """
        if self._original_df is None:
            raise ValueError("DataFrame not set. Please load the data first.")
        try:
            # Enclose column names with spaces in backticks
            for col in self._original_df.columns:
                if ' ' in col and f'`{col}`' not in condition:
                    condition = condition.replace(col, f'`{col}`')

            filtered = self._original_df.query(condition)
            std_condition = condition

            if std_condition:
                filtered, info = check_shrink_df(filtered, MAX_ROWS, std_condition)
            else:
                filtered, info = check_shrink_df(filtered, MAX_ROWS)
            self.df = filtered
            return info
        except Exception as e:
            return f"Error filtering data with condition '{condition}': {str(e)}"

