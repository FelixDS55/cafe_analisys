import sqlite3
import pandas as pd

connection = sqlite3.connect('cafe.db')

df = pd.read_excel('group 10 mnth.xlsx')
df.to_sql('group', connection, index=False, if_exists='replace')
connection.commit()
connection.close()
print('Data upload')