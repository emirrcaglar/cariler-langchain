import pandas as pd
from src.my_tools import DataFrameHandler

data = 'data/cari_hesap_hareketleri.csv'

df = DataFrameHandler(data)

print(df.get_column_names())
