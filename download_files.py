import sqlite3
import pandas as pd
import csv
import glob
import os

path = r'C:\projects\Cafe\files'


def read_files():
    files = glob.glob(os.path.join(path, "*.csv"))
    combined_df = pd.DataFrame()

    for file in files:
        df = pd.read_csv(file, header=None, encoding='windows-1251', delimiter=';')
        combined_df = pd.concat([combined_df, df], ignore_index=True)

    columns_name = ['rnm', 'fn', 'address', 'fp', 'num_check', 'type_fd', 'prihod', 'datetime', 'smena',
                    'good', 'priznak_predmet', 'total_chek', 'cash', 'card', 'avans', 'zachet_avans', 'postoplata',
                    'vstrechymi', 'price', 'amount', 'position_good',
                    'sum_bez_nds', 'sum_nds_0', 'sum_nds_10', 'sum_nds_20', 'sum_nds_10/110', 'sum_nds_18/118',
                    'sum_nds_20/120', 'sum_good', 'sposob_raschet',
                    'nds_good_prc', 'nds_good', 'agent', 'inn', 'postavshik']

    combined_df.columns = columns_name

    filtered_df = combined_df[~combined_df['good'].str.contains('Фуршет|Пирожки|Виноградова|манипул|Титоренко', na=False)]

    filtered_df.to_csv('6_month.csv', index=False)
    print('File create')


def write_to_db():
    columns_to_use = ['rnm', 'fn', 'fp', 'num_check', 'type_fd', 'datetime', 'smena',
                      'good', 'total_chek', 'cash', 'card', 'price', 'amount', 'position_good',
                      'sum_nds_20', 'sum_good', 'nds_good_prc', 'nds_good',]

    df = pd.read_csv('6_month.csv', usecols=columns_to_use, sep=',')

    df['summa'] = df['cash'] + df['card']

    df['payment'] = df['cash'].apply(lambda x: 'cash' if x > 0 else 'card')
    df['check_unique'] = df['num_check'].astype(str) + ' - ' + df['rnm'].astype(str)

    connection = sqlite3.connect('cafe.db')
    # cursor = connection.cursor()

    df['datetime'] = pd.to_datetime(df['datetime'], format='%d.%m.%Y %H:%M')
    df.to_sql('cafe', connection, index=False, if_exists='replace')
    connection.commit()
    connection.close()
    print('Data upload')


def download_group():
    df = pd.read_csv('Group.csv', sep=';')
    connection = sqlite3.connect('cafe.db')
    df.to_sql('group', connection, index=False, if_exists='replace')
    connection.commit()
    connection.close()
    print('Data upload')


read_files()
write_to_db()
# download_group()
