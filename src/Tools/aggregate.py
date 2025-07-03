import pandas as pd
from pydantic import Field
from langchain.tools import BaseTool
from typing import List, Any, Optional

from src.utils import check_shrink_df
from src.constants import MAX_ROWS


class DataFrameAggregateTool(BaseTool):
    name: str = "dataframe_aggregator"
    description: str = """Useful for grouping and aggregating DataFrame data. 
    Input should be a JSON string with two keys: 
    'action' -the function to run ('apply_aggregation'), 
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

        preview_df = self.grouped_data.size().reset_index(name='Count')
        _, info = check_shrink_df(preview_df, MAX_ROWS, f"grouped by {columns}")

        return f"Successfully grouped by {columns}.\nGroup sizes preview:\n{info}\nNow apply an aggregation function."

    def _apply_aggregation(self, function: str) -> str:
        """Apply aggregation to previously grouped data."""
        if self.grouped_data is None:
            return "Error: You must group data first using 'group_by'."
        try:
            result_df = self.grouped_data.agg(function)
            check_shrink_df(result_df, MAX_ROWS)

            return f"Aggregation result ({function}): \n {result_df.to_string()}"
        except Exception as e:
            return f"Aggregation failed: {str(e)}"
