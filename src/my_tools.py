from langchain.tools import BaseTool
from langchain_chroma import Chroma

import io
import difflib
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
                return self._describe_column(params['column_name'].strip())
            elif action == "get_value_counts":
                return self._get_value_counts(params['column_name'].strip())
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

    def _describe_column(self, column_name: str):
        """Get descriptive statistics for a specific column (count, mean, std, min, max, etc.)"""
        if self.df is None:
            return "DataFrame not set. Please load the data first."
        if column_name not in self.df.columns:
            return f"Column '{column_name} not found. Available columns: {list(self.df.columns)}"
        return self.df[column_name].describe().to_string()

    def _get_value_counts(self, column_name: str, normalize=False):
        """Get frequency counts of unique values in a column. Useful to know what values are present in a column and how many times they occur."""
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
    and 'params' ('columns' for select_columns, 'condition' for filter_data)."""   

    df: pd.DataFrame = Field(..., description="The pandas DataFrame to transform")
    error_memory: List[dict] = Field(default_factory=list, description="Memory to store errors for repeated inputs")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.error_memory: List[dict] = []

    def _run(self, tool_input: str) -> str:
        """Main execution method required by BaseTool"""
        # Count how many times this input has caused an error
        error_count = sum(1 for error in self.error_memory if error['input'] == tool_input)
        if error_count >= 3:
            return f"Repeated error for input: {tool_input}. Skipping after 3 errors."
        try:
            import json
            data = json.loads(tool_input)
            action = data['action']
            params = data['params']

            if action == "select_columns":
                return self._select_columns([col.strip() for col in params['columns']])
            elif action == "filter_data":
                return self._filter_data(params['condition'].strip())
            return "Invalid action. Use either 'group_by' or 'apply_aggregation'"
        except Exception as e:
            error_message = f"Error processing input: {str(e)}"
            self.error_memory.append({'input': tool_input, 'error': error_message})
            return error_message

    def _select_columns(self, columns: List[str]):
        """Select listed columns. This will modify the global DataFrame to contain only these columns."""
        if self.df is None:
            return "DataFrame not set. Please load the data first."
        # Normalize DataFrame columns
        df_cols = [col.upper().replace(" ", "_") for col in self.df.columns]
        # Normalize input columns
        columns_norm = [col.upper().replace(" ", "_") for col in columns]
        missing = [col for col in columns_norm if col not in df_cols]
        if missing:
            suggestions = []
            for col in missing:
                match = difflib.get_close_matches(col, df_cols, n=1)
                if match:
                    suggestions.append(f"{col} (did you mean {match[0]}?)")
                else:
                    suggestions.append(col)
            return f"Column(s) {suggestions} not found. Available columns: {df_cols}"
        # Select columns using original names
        selected = [self.df.columns[df_cols.index(col)] for col in columns_norm]
        self.df = self.df[selected]
        return f"DataFrame updated with selected columns: {selected}.\n{self.df.to_string()}"

    def _filter_data(self, condition: str):
        if self.df is None:
            raise ValueError("DataFrame not set. Please load the data first.")
        self.df = self.df.query(condition)
        return f"DataFrame filtered by condition '{condition}'.\n{self.df.to_string()}"


class DataFrameAggregateTool(BaseTool):
    name: str = "dataframe_aggregator"
    description: str = """Useful for grouping and aggregating DataFrame data. 
    Input should be a JSON string with two keys: 
    'action' ('apply_aggregation'), 
    and 'params' (dictionary with 'group_by' and 'aggregation').
    'group_by' should be a list of column names to group by,
    aggregation should be a string like "min", "sum", etc.)"""
    df: pd.DataFrame = Field(..., description="The pandas DataFrame to aggregate")
    grouped_data: Optional[Any] = Field(None, description="Stores grouped data for aggregation")

    def _run(self, tool_input: str) -> str:
        """Main execution method required by BaseTool"""
        try:
            import json
            data = json.loads(tool_input)
            action = data['action']
            params = data['params']

            if not params['group_by']:
                try:
                    result = self.df.agg(params['aggregation'])
                    return f"Aggregation result (no group): \n {result.to_string()}"
                except Exception as e:
                    return f"Aggregation failed: {str(e)}"
            if action == "apply_aggregation":
                self._group_by([col.strip() for col in params['group_by']])
                return self._apply_aggregation(params['aggregation'])
            return "Invalid action. Use 'apply_aggregation'"
        except Exception as e:
            return f"Error processing input: {str(e)}"
            
    def _group_by(self, columns: List[str]) -> str:        
        """
        Group the data by given columns.
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
    name: str = "dataframe_analyzer"
    description: str = """Useful for semantically analyzing DataFrame. 
    Input should be a JSON string with two keys: 
    'action' ('similarity_search'), 
    and 'params' (dictionary of parameters)."""
    df: pd.DataFrame = Field(..., description="The pandas DataFrame to analyze")
    vectorstore: Chroma = Field(..., description="The vectorstore to analyze")

    def _run(self, tool_input: str) -> str:
        """Main execution method required by BaseTool"""
        try:
            import json
            data = json.loads(tool_input)
            action = data['action']
            params = data['params']

            if action == "similarity_search":
                return self._similarity_search(params['columns'].strip())
            return "Invalid action. Use either 'group_by' or 'apply_aggregation'"
        except Exception as e:
            return f"Error processing input: {str(e)}"

    def _similarity_search(self, query: str, k: int = 3):
        """Perform a similarity search on the vector store for a given query."""
        if self.vectorstore is None:
            return "Vectorstore not set. Please load the data first."
        results = self.vectorstore.similarity_search(query, k=k)
        return "\n".join([doc.page_content for doc in results])
