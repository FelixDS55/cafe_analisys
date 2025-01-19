import warnings
import pandas as pd
import glob
import os
import sqlite3

path = r'C:\Users\TurilovMA\Desktop\Projects\Cafe\pythonProject\realiz'

files = glob.glob(os.path.join(path, '*.xlsx'))
combined_df = pd.DataFrame()
connection = sqlite3.connect('cafe.db')

for item in files:
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        df = pd.read_excel(item, engine='openpyxl', sheet_name=1)
    new_col = item.split()
    date_value = new_col[-1].replace('.xlsx', '')
    df['period'] = date_value
    combined_df = pd.concat([combined_df, df], ignore_index=True)
    # print(combined_df['period'])


# print(combined_df['period'])
our_cols = ['Товар', 'Закупочные суммы', 'period']

combined_df = combined_df[our_cols]

combined_df = combined_df[~combined_df['Товар'].isna()]

combined_df['Закупочные суммы'] = combined_df['Закупочные суммы'].astype(float)
combined_df['period'] = pd.to_datetime(combined_df['period'], dayfirst=True)

combined_df = combined_df.rename(columns={'Товар': 'good', 'Закупочные суммы': 'zakup_sum'})

file = combined_df.to_csv('Price_avg.csv', index=False)
combined_df.to_sql('price_avg', connection, index=False, if_exists='replace')
