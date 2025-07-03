import pandas as pd
import pytest

from src.Tools.filter import DataFrameFilterTool
from src.Tools.aggregate import DataFrameAggregateTool  # Assuming this is the correct import path

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "A": [1, 2, 3],
        "B": ["x", "y", "z"]
    })

def test_select_columns(sample_df):
    tool = DataFrameFilterTool(df=sample_df)
    input_json = '{"action": "select_columns", "params": {"columns": ["A"]}}'
    result = tool._run(input_json)
    assert "DataFrame updated" in result
    assert list(tool.df.columns) == ["A"]

def test_filter_data(sample_df):
    tool = DataFrameFilterTool(df=sample_df)
    input_json = '{"action": "filter_data", "params": {"condition": "A > 1"}}'
    result = tool._run(input_json)
    assert "filtered by condition" in result

def test_error_memory(sample_df):
    tool = DataFrameFilterTool(df=sample_df)
    bad_input = '{"action": "filter_data", "params": {"condition": "BAD SYNTAX"}}'
    # Run 3 times to accumulate errors
    tool._run(bad_input)
    tool._run(bad_input)
    tool._run(bad_input)
    # 4th run should trigger skip
    result = tool._run(bad_input)
    assert "Repeated error" in result
    assert "Skipping after 3 errors" in result

def test_aggregate_columns(sample_df):
    tool = DataFrameAggregateTool(df=sample_df) #type: ignore
    input_json = '{"action": "apply_aggregation", "params": {"columns": ["A"], "aggregation": {"min": "A"}}}'
    result = tool._run(input_json)
    assert "Aggregation result" in result
    assert "A" in result  # Check if the column is present in the result


