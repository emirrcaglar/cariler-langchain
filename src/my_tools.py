from langchain.tools import BaseTool
from langchain_chroma import Chroma

import io
import pandas as pd
from pydantic import Field
from dotenv import load_dotenv
from typing import List, Any, Optional
import re

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

class DataFrameFilterTool(BaseTool):
    name: str = "dataframe_transformer"
    description: str = """Useful for transforming and filtering DataFrame data. 
    Input should be a JSON string with two keys: 
    'action' ('filter_data'), 
    and 'params' ('columns' for select_columns, 'condition' for filter_data)."""   

    df: pd.DataFrame = Field(..., description="The pandas DataFrame to filter")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
        if self.df is None:
            raise ValueError("DataFrame not set. Please load the data first.")
        try:
            # Handle LLM-generated .str.contains() expressions directly
            str_contains_pattern = r"([\w\s]+)\.str\.contains\(['\"](.+?)['\"],?\s*case\s*=\s*(True|False)?"
            str_contains_match = re.match(str_contains_pattern, condition, re.IGNORECASE)
            if str_contains_match:
                col = str_contains_match.group(1).strip()
                val = str_contains_match.group(2).strip()
                case = str_contains_match.group(3)
                case = False if case and case.lower() == "false" else True
                filtered = self.df[self.df[col].str.contains(val, case=case, na=False)]
                std_condition = f"{col}.str.contains('{val}', case={case})"
            else:
                # Regex to match: column op value (e.g., `Col` == 'val', Col contains val)
                pattern = r'([`"\']?)([\w\s]+)\1\s*([=!<>]+|contains)\s*([`"\']?)([^`"\']+)\4'
                match = re.match(pattern, condition, re.IGNORECASE)
                if match:
                    col = match.group(2).strip()
                    op = match.group(3).strip().lower()
                    val = match.group(5).strip()
                    if op == "contains":
                        filtered = self.df[self.df[col].str.contains(val, case=False, na=False)]
                        std_condition = f"{col}.str.contains('{val}')"
                    elif val.replace('.', '', 1).isdigit():
                        std_condition = f"`{col}` {op} {val}"
                        filtered = self.df.query(std_condition)
                    else:
                        std_condition = f"`{col}` {op} '{val}'"
                        filtered = self.df.query(std_condition)
                else:
                    # fallback: remove backticks and double quotes, use query
                    std_condition = re.sub(r"[`\"\\]", "", condition)
                    filtered = self.df.query(std_condition)
            self.df = filtered
            print(f"DataFrame filtered by standardized condition '{std_condition}'.\n{self.df.to_string()}")
            return f"DataFrame filtered by standardized condition '{std_condition}'.\n{self.df.to_string()}"
        except Exception as e:
            return f"Error filtering data with condition '{condition}': {str(e)}"
        

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
