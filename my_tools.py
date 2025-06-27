from typing import List
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
def select_columns(cols: List[str]):
    """Select listed columns. This will create a new data object that stores all the data of the specified columnns."""
    if df is None:
        return "DataFrame not set. Please load the data first."  
    for col in cols: 
        if col not in df.columns:
            return f"Column '{col} not found. Available columns: {list(df.columns)}"    
    return df[cols].to_string()


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
def describe_column(column_name: str):
    """Get descriptive statistics for a specific column (count, mean, std, min, max, etc.)"""
    if df is None:
        return "DataFrame not set. Please load the data first."
    if column_name not in df.columns:
        return f"Column '{column_name} not found. Available columns: {list(df.columns)}"
    return df[column_name].describe().to_string()

@tool
def filter_data(condition: str):
    """Filter the data based on a condition (e.g., 'age > 30')"""
    if df is None:
        return "DataFrame not set. Please load the data first."
    try:
        filtered_df = df.query(condition)
        return filtered_df.to_string()
    except Exception as e:
        return f"Error filtering data: {e}"

@tool
def get_value_counts(column_name: str, normalize=False):
    """Get frequency counts of unique values in a column"""
    if df is None:
        return "DataFrame not set. Please load the data first."   
    if column_name not in df.columns:
        return f"Column '{column_name} not found. Available columns: {list(df.columns)}"   
    return df[column_name].value_counts(normalize=normalize).to_string()

@tool
def group_by(cols: List[str]):
    """
    Group the data by given columns.
    A groupby operation involves some combination of splitting the object, applying a function, and combining the results. 
    This can be used to group large amounts of data and compute operations on these groups.
    """
    if df is None:
        return "DataFrame not set. Please load the data first."  
    for col in cols: 
        if col not in df.columns:
            return f"Column '{col} not found. Available columns: {list(df.columns)}"   
    global grouped_df
    grouped_df = df.groupby(cols)
    return f"Successfully grouped by {cols}. Now, use the 'apply_aggregation' tool to specify a calculation. (e.g., 'sum', 'mean')"

@tool
def apply_aggregation(aggregation_function: str):
    """
    Step 2 of an aggregation. Applies a calculation to the data previously grouped by 'group_by' tool.
    Args: 
        aggregation_function (str): The calculation to perform (e.g., 'sum', 'mean', 'count')
    """
    global grouped_df
    if grouped_df is None:
        return "Error: You must use the 'group_by' tool before applying an aggregation." 
    try:
        result_df = grouped_df.agg(aggregation_function)
        return result_df.to_string()
    except Exception as e:
        return f"An error occured during aggregation: {e}"

@tool
def math_operation(operation: str, numbers: List[float]) -> float:
    """Perform mathematical operations on a list of numbers.
    Supported operations: 'add', 'average'.
    Example: math_operation('add', [1,2,3]) returns 6."""
    if not numbers:
        return 0.0
    try:
        if operation == 'add':
            return sum(numbers)
        elif operation == 'average':
            return sum(numbers) / len(numbers)
        else:
            raise ValueError(f"Unsupported operation: {operation}")
    except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid operation: {operation}")

@tool
def similarity_search(query: str, k: int = 3):
    """Perform a similarity search on the vector store for a given query."""
    if vectorstore is None:
        return "Vectorstore not set. Please load the data first."
    results = vectorstore.similarity_search(query, k=k)
    return "\n".join([doc.page_content for doc in results])
