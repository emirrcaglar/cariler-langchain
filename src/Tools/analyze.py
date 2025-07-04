import pandas as pd
from pydantic import Field
from langchain.tools import BaseTool
from langchain_chroma import Chroma


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
        if k > 10:
            k = 10
        results = self.vectorstore.similarity_search(query, k=k)
        return "\n".join([doc.page_content for doc in results])
