from pydantic import Field
from langchain.tools import BaseTool
import pandas as pd
import io

class DataFrameInspectTool(BaseTool):
    """Tools for inspecting DataFrame structure"""
    name: str = "dataframe_inspector"
    description: str = """Useful for inspecting the DataFrame and it's structure. 
    Input should be a JSON string with two keys: 
    'action' (either 'get_column_names', 'get_head', 'get_info', 'describe_column' or 'get_value_counts'), 
    and 'params' (dictionary of parameters)."""   
    df: pd.DataFrame = Field(..., description="The pandas DataFrame to inspect")

    def _run(self, tool_input: str):
        """Main execution method required by BaseTool"""
        try:
            import json
            data = json.loads(tool_input)
            action = data['action']
            params = data['params']

            if action == "get_column_names":
                return self._get_column_names()
            elif action == "get_head":
                return self._get_head(params['n'])
            elif action == "get_info":
                return self._get_info()
            elif action == "describe_column":
                return self._describe_column(params['column'].strip())
            elif action == "get_value_counts":
                return self._get_value_counts(params['column'].strip())
            return "Invalid action. Use either 'group_by' or 'apply_aggregation'"
        except Exception as e:
            return f"Error processing input: {str(e)}"

    def _get_column_names(self):
        """Get the names of all the columns from the dataframe."""
        if self.df is None:
            return "DataFrame not set. Please load the data first."
        return list(self.df.columns.values)

    def _get_head(self, column_count: int = 5):
        """Get the first {column_count} rows of the dataframe. Returns the rows as a string."""
        if self.df is None:
            return "DataFrame not set. Please load the data first."
        return self.df.head(column_count).to_string()

    def _get_info(self):
        """Get a concise summary of the dataframe, including the index dtype and columns, non-null values, and memory usage."""
        if self.df is None:
            return "DataFrame not set. Please load the data first."
        buffer = io.StringIO()
        self.df.info(buf=buffer)
        return buffer.getvalue()

    def _describe_column(self, column: str):
        """Get descriptive statistics for a specific column (count, mean, std, min, max, etc.)"""
        if self.df is None:
            return "DataFrame not set. Please load the data first."
        if column not in self.df.columns:
            return f"Column '{column} not found. Available columns: {list(self.df.columns)}"
        return self.df[column].describe().to_string()

    def _get_value_counts(self, column: str, normalize=False):
        """Get frequency counts of unique values in a column. Useful to know what values are present in a column and how many times they occur."""
        if self.df is None:
            return "DataFrame not set. Please load the data first."   
        if column not in self.df.columns:
            return f"Column '{column} not found. Available columns: {list(self.df.columns)}"   
        return self.df[column].value_counts(normalize=normalize).to_string()