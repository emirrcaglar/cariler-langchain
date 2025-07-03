import pandas as pd
import re
from pydantic import Field, PrivateAttr
from langchain.tools import BaseTool


class DataFrameFilterTool(BaseTool):
    name: str = "dataframe_transformer"
    description: str = """Useful for transforming and filtering DataFrame data. 
    Input should be a JSON string with two keys: 
    'action' ('filter_data'), 
    and 'params' ('columns' for select_columns, 'condition' for filter_data)."""   

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
        Supports 'contains' operator using pandas str.contains.
        Also supports LLM-generated .str.contains() expressions.
        """
        if self._original_df is None:
            raise ValueError("DataFrame not set. Please load the data first.")
        try:
            # Handle LLM-generated .str.contains() expressions directly
            str_contains_pattern = r"""([\w\s]+)\.str\.contains\((['"])(.+?)\2(?:,\s*case\s*=\s*(True|False))?\)"""
            str_contains_match = re.match(str_contains_pattern, condition, re.IGNORECASE)
            if str_contains_match:
                col = str_contains_match.group(1).strip()
                val = str_contains_match.group(3).strip()
                case = str_contains_match.group(4)
                case = False if case and case.lower() == "false" else True
                filtered = self._original_df[self._original_df[col].str.contains(val, case=case, na=False)]
                std_condition = f"{col}.str.contains('{val}', case={case})"
            else:
                # Regex to match: column op value (e.g., `Col` == 'val', Col contains val)
                pattern = r"([`\"']?)([\w\s]+)\1\s*([=!<>]+|contains)\s*([`\"']?)([^`\"']+)\4"
                match = re.match(pattern, condition, re.IGNORECASE)
                if match:
                    col = match.group(2).strip()
                    op = match.group(3).strip().lower()
                    val = match.group(5).strip()
                    if op == "contains":
                        filtered = self._original_df[self._original_df[col].str.contains(re.escape(val), case=True, na=False)]
                        std_condition = f"{col}.str.contains('{val}')"
                    elif val.replace('.', '', 1).isdigit():
                        std_condition = f"`{col}` {op} {val}"
                        filtered = self._original_df.query(std_condition)
                    else:
                        std_condition = f"`{col}` {op} '{val}'"
                        filtered = self._original_df.query(std_condition)
                else:
                    # fallback: use the condition directly as a pandas query
                    std_condition = condition
                    filtered = self._original_df.query(std_condition)
            self.df = filtered
            print(f"DataFrame filtered by standardized condition '{std_condition}'.\n{self.df.to_string()}")
            return f"DataFrame filtered by standardized condition '{std_condition}'.\n{self.df.to_string()}"
        except Exception as e:
            return f"Error filtering data with condition '{condition}': {str(e)}"

