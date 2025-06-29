from langchain.tools import BaseTool

import io
import pandas as pd
from pydantic import Field
from dotenv import load_dotenv
from typing import List, Any, Optional

load_dotenv()

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
                return self._describe_column(params['column_name'])
            elif action == "get_value_counts":
                return self._get_value_counts(params['column_name'])
            return "Invalid action. Use either 'group_by' or 'apply_aggregation'"
        except Exception as e:
            return f"Error processing input: {str(e)}"

    def _get_column_names(self):
        """Get the names of all the columns from the dataframe."""
        if self.df is None:
            return "DataFrame not set. Please load the data first."
        return list(self.df.columns.values)

    def _get_head(self, n: int = 5):
        """Get the first n rows of the dataframe. Returns the rows as a string."""
        if self.df is None:
            return "DataFrame not set. Please load the data first."
        return self.df.head(n).to_string()

    def _get_info(self):
        """Get a concise summary of the dataframe, including the index dtype and columns, non-null values, and memory usage."""
        if self.df is None:
            return "DataFrame not set. Please load the data first."
        buffer = io.StringIO()
        self.df.info(buf=buffer)
        return buffer.getvalue()

    def _describe_column(self, column_name: str):
        """Get descriptive statistics for a specific column (count, mean, std, min, max, etc.)"""
        if self.df is None:
            return "DataFrame not set. Please load the data first."
        if column_name not in self.df.columns:
            return f"Column '{column_name} not found. Available columns: {list(self.df.columns)}"
        return self.df[column_name].describe().to_string()

    def _get_value_counts(self, column_name: str, normalize=False):
        """Get frequency counts of unique values in a column"""
        if self.df is None:
            return "DataFrame not set. Please load the data first."   
        if column_name not in self.df.columns:
            return f"Column '{column_name} not found. Available columns: {list(self.df.columns)}"   
        return self.df[column_name].value_counts(normalize=normalize).to_string()


class DataFrameTransformTool(BaseTool):
    name: str = "dataframe_transformer"
    description: str = """Useful for transforming and filtering DataFrame data. 
    Input should be a JSON string with two keys: 
    'action' (either 'select_columns' or 'filter_data'), 
    and 'params' (dictionary of parameters)."""   

    df: pd.DataFrame = Field(..., description="The pandas DataFrame to transform")


    def _run(self, tool_input: str) -> str:
        """Main execution method required by BaseTool"""
        try:
            import json
            data = json.loads(tool_input)
            action = data['action']
            params = data['params']

            if action == "select_columns":
                return self._select_columns(params['columns'])
            elif action == "filter_data":
                return self._filter_data(params['condition'])
            return "Invalid action. Use either 'group_by' or 'apply_aggregation'"
        except Exception as e:
            return f"Error processing input: {str(e)}"


    def _select_columns(self, columns: List[str]):
        """Select listed columns. This will modify the global DataFrame to contain only these columns."""
        if self.df is None:
            return "DataFrame not set. Please load the data first."  
        for col in columns: 
            if col not in self.df.columns:
                return f"Column '{col} not found. Available columns: {list(self.df.columns)}"    
        self.df = self.df[columns]
        return f"DataFrame updated. Now contains only columns: {columns}."


    def _filter_data(self, condition: str):
        """Filter the data based on a condition (e.g., 'age > 30'). This will modify the global DataFrame."""
        if self.df is None:
            return "DataFrame not set. Please load the data first."
        try:
            df = self.df.query(condition)
            return f"DataFrame filtered by condition: '{condition}'."
        except Exception as e:
            return f"Error filtering data: {e}"


class DataFrameAggregateTool(BaseTool):
    name: str = "dataframe_aggregator"
    description: str = """Useful for grouping and aggregating DataFrame data. 
    Input should be a JSON string with two keys: 
    'action' (either 'group_by' or 'apply_aggregation'), 
    and 'params' (dictionary of parameters)."""
    df: pd.DataFrame = Field(..., description="The pandas DataFrame to analyze")
    grouped_data: Optional[Any] = Field(None, description="Stores grouped data for aggregation")

    def _run(self, tool_input: str) -> str:
        """Main execution method required by BaseTool"""
        try:
            import json
            data = json.loads(tool_input)
            action = data['action']
            params = data['params']

            if action == "group_by":
                return self._group_by(params['columns'])
            elif action == "apply_aggregation":
                return self._apply_aggregation(params['function'])
            return "Invalid action. Use either 'group_by' or 'apply_aggregation'"
        except Exception as e:
            return f"Error processing input: {str(e)}"
    def _group_by(self, columns: List[str]) -> str:        
        """
        Group the data by given columns.
        A groupby operation involves some combination of splitting the object, applying a function, and combining the results. 
        This can be used to group large amounts of data and compute operations on these groups.
        """
        if self.df.empty:
            return "DataFrame is empty. Please load valid data first."  

        missing_cols = [col for col in columns if col not in self.df.columns]
        if missing_cols:
            return f"Columns {missing_cols} not found. Available columns: {list(self.df.columns)}"

        self.grouped_data = self.df.groupby(columns)
        return f"Successfully grouped by {columns}. Now apply an aggregation function."

    def _apply_aggregation(self, function: str) -> str:
        """Apply aggregation to previously grouped data."""
        if self.grouped_data is None:
            return "Error: You must group data first using 'group_by'."
        try:
            result_df = self.grouped_data.agg(function)
            return f"Aggregation result ({function}): \n {result_df.to_string()}"
        except Exception as e:
            return f"Aggregation failed: {str(e)}"







class DataFrameAnalysisTool(BaseTool):

    def __init__(self, data, vectorstore=None):
        self.df = pd.read_csv(data)
        self.vectorstore = vectorstore




    # def similarity_search(query: str, k: int = 3):
    #     """Perform a similarity search on the vector store for a given query."""
    #     if vectorstore is None:
    #         return "Vectorstore not set. Please load the data first."
    #     results = vectorstore.similarity_search(query, k=k)
    #     return "\n".join([doc.page_content for doc in results])
