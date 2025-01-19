import sqlite3
import warnings

import openpyxl
import pandas as pd
import csv
import glob
import os

path = r'C:\projects\Cafe\reales'

files = glob.glob(os.path.join(path, "*.xlsx"))

with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    book = pd.read_excel(r'C:\projects\Cafe\reales\Акт реализации с 01.01.2024 по 31.01.2024.xlsx', sheet_name=1,
                         engine='openpyxl')

new_column = files[0].split()[len(files[0].split()) - 1]
new_column = new_column.replace('.xlsx', '')

new_book = book[['Товар', 'Закупочные суммы']].copy()
new_book.loc[:, 'month'] = new_column


print(new_book)

# print(new_book[new_book['Товар'] == 'Сырник'])
