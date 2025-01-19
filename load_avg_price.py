import sqlite3
import pandas as pd
import openpyxl
import sqlite3

path = r'C:\projects\Cafe\avg_price\avg_price_all.xlsx'

connection = sqlite3.connect('cafe.db')

df = pd.read_excel(path)

df['period'] = pd.to_datetime(df['period'])

df.to_sql('avg_price_all', connection, index=False, if_exists='replace')

print(df)
