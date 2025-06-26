from langchain.tools import tool
import pandas as pd
import io

# Global variables for dependencies
df = None
vectorstore = None

def set_dataframe(data: pd.DataFrame):
    """Sets the global dataframe for the pandas tools to use."""
    global df
    df = data

def set_vectorstore(vs):
    """Sets the global vectorstore for the search tool to use."""
    global vectorstore
    vectorstore = vs

@tool
def get_column_names():
    """Get the names of all the columns from the dataframe."""
    if df is None:
        return "DataFrame not set. Please load the data first."
    return list(df.columns.values)

@tool
def get_head(n: int = 5):
    """Get the first n rows of the dataframe. Returns the rows as a string."""
    if df is None:
        return "DataFrame not set. Please load the data first."
    return df.head(n).to_string()

@tool
def get_info():
    """Get a concise summary of the dataframe, including the index dtype and columns, non-null values, and memory usage."""
    if df is None:
        return "DataFrame not set. Please load the data first."
    buffer = io.StringIO()
    df.info(buf=buffer)
    return buffer.getvalue()

@tool
def similarity_search(query: str, k: int = 3):
    """Perform a similarity search on the vector store for a given query."""
    if vectorstore is None:
        return "Vectorstore not set. Please load the data first."
    results = vectorstore.similarity_search(query, k=k)
    return "\n".join([doc.page_content for doc in results])
