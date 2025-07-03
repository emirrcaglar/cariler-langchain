import pandas as pd
import pytest
from src.Tools.filter import DataFrameFilterTool

@pytest.fixture
def sample_dataframe():
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Ayşe', 'Ömer'],
        'Age': [25, 30, 35, 40, 45, 28, 32],
        'City': ['New York', 'London', 'Paris', 'New York', 'London', 'İstanbul', 'İzmir'],
        'Salary': [50000, 60000, 75000, 80000, 90000, 55000, 70000]
    }
    return pd.DataFrame(data)

def test_filter_data_float_equality():
    df = pd.DataFrame({'Value': [10.0, 20.0, 30.0, 20.00000000000001]})
    tool = DataFrameFilterTool(df=df)
    tool._filter_data("Value == 20.0")
    assert len(tool.df) == 2
    assert 20.0 in tool.df['Value'].tolist()

def test_filter_data_contains(sample_dataframe):
    tool = DataFrameFilterTool(df=sample_dataframe)
    tool._filter_data("Name contains 'li'")
    assert len(tool.df) == 2
    assert set(tool.df["Name"]) == {"Alice", "Charlie"}

def test_filter_data_str_contains_case_sensitive(sample_dataframe):
    tool = DataFrameFilterTool(df=sample_dataframe)
    tool._filter_data("Name.str.contains('alice', case=True)")
    assert len(tool.df) == 0

def test_filter_data_str_contains_case_insensitive(sample_dataframe):
    tool = DataFrameFilterTool(df=sample_dataframe)
    tool._filter_data("Name.str.contains('alice', case=False)")
    assert len(tool.df) == 1
    assert tool.df['Name'].iloc[0] == 'Alice'

def test_filter_data_equals_string(sample_dataframe):
    tool = DataFrameFilterTool(df=sample_dataframe)
    tool._filter_data("City == 'New York'")
    assert len(tool.df) == 2
    assert 'Alice' in tool.df['Name'].tolist()
    assert 'David' in tool.df['Name'].tolist()

def test_filter_data_greater_than_numeric(sample_dataframe):
    tool = DataFrameFilterTool(df=sample_dataframe)
    tool._filter_data("Age > 30")
    assert len(tool.df) == 4
    assert 'Charlie' in tool.df['Name'].tolist()
    assert 'David' in tool.df['Name'].tolist()
    assert 'Eve' in tool.df['Name'].tolist()
    assert 'Ömer' in tool.df['Name'].tolist()

def test_filter_data_less_than_numeric(sample_dataframe):
    tool = DataFrameFilterTool(df=sample_dataframe)
    tool._filter_data("Salary < 70000")
    assert len(tool.df) == 3
    assert 'Alice' in tool.df['Name'].tolist()
    assert 'Bob' in tool.df['Name'].tolist()
    assert 'Ayşe' in tool.df['Name'].tolist()

def test_filter_data_invalid_condition(sample_dataframe):
    tool = DataFrameFilterTool(df=sample_dataframe)
    result = tool._filter_data("InvalidColumn == 'test'")
    assert "Error filtering data" in result

def test_run_filter_data_action(sample_dataframe):
    tool = DataFrameFilterTool(df=sample_dataframe)
    tool_input = '{"action": "filter_data", "params": {"condition": "Age > 30"}}'
    result = tool._run(tool_input)
    assert "DataFrame filtered by standardized condition '`Age` > 30'" in result
    assert len(tool.df) == 4
    tool = DataFrameFilterTool(df=sample_dataframe)
    tool_input = '{"action": "invalid_action", "params": {"condition": "Age > 30"}}'
    result = tool._run(tool_input)
    assert "Invalid action" in result

def test_run_invalid_json_input(sample_dataframe):
    tool = DataFrameFilterTool(df=sample_dataframe)
    tool_input = '{"action": "filter_data", "params": {"condition": "Age > 30"' # Malformed JSON
    result = tool._run(tool_input)
    assert "Error processing input" in result
