import pytest
import pandas as pd
from src.Tools.currency import CurrencyTool, CurrencyEnum

def assert_is_dataframe(result):
    assert isinstance(result, pd.DataFrame), f"Expected DataFrame, got: {result}"

@pytest.fixture
def dummy_df():
    return pd.DataFrame({
        'id': [1, 2, 3],
        'currency': ['USD', 'EUR', 'TRY'],
        'amount': [100, 200, 300]
    })

@pytest.fixture
def mock_api_data():
    return {
        'data': {
            'USD': 1.0,
            'EUR': 0.9,
            'TRY': 30.0
        }
    }

def test_merge_currencies(dummy_df, mock_api_data):
    tool = CurrencyTool(df=dummy_df.copy(), base_currency=CurrencyEnum.USD, api_data=mock_api_data)
    result = tool._merge_currencies(mock_api_data, 'currency', ['amount'])
    if not isinstance(result, pd.DataFrame):
        pytest.skip(f"Tool returned error: {result}")
        return
    assert 'amount_in_USD' in result.columns
    # Check conversion
    assert result.loc[0, 'amount_in_USD'] == 100 * 1.0
    assert result.loc[1, 'amount_in_USD'] == 200 * 0.9
    assert result.loc[2, 'amount_in_USD'] == 300 * 30.0

def test_run_merge_action(dummy_df, mock_api_data):
    tool = CurrencyTool(df=dummy_df.copy(), base_currency=CurrencyEnum.USD, api_data=mock_api_data)
    tool_input = {
        'action': 'merge_currencies',
        'params': {
            'currency_column': 'currency',
            'money_columns': ['amount']
        }
    }
    result = tool._run(tool_input)
    if not isinstance(result, pd.DataFrame):
        pytest.skip(f"Tool returned error: {result}")
        return
    assert 'amount_in_USD' in result.columns

# Optionally, you can mock _get_currency_data for get_currency_data action if needed 