#!/usr/bin/env python

import pandas as pd
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
import csv
from io import StringIO




class Transform_pse:

    def __init__(self, df):
        self.df = df



    def transform_date_time_pse(self):
        doba = self.df.iloc[:, 0]
        doba_name = self.df.iloc[:, 0].name
        data_pub = self.df.iloc[:, 1]
        data_pub_name = self.df.iloc[:, 1].name
        tr_doba = pd.to_datetime(doba, format = "%Y-%m-%d")
        tr_data_pub = pd.to_datetime(data_pub, format = "%Y%m%d%H%M%S")
        df = self.df.drop(columns=[doba_name, data_pub_name])
        df.insert(0, doba_name, tr_doba)
        df.insert(0, data_pub_name, tr_data_pub)
        return df

    def transform_unpivot_hours_pse(self, df):
        df_unpivoted = df.melt(id_vars=['Data publikacji', 'Doba', 'Kod', 'Nazwa', 'Tryb pracy'],
            value_vars=df.columns[-24:],
            var_name='Godzina', value_name='Wolumen')
        return df_unpivoted





class Transform_kse_or_pse:

    def __init__(self, response):
        self.response = response

    def pse_or_kse_to_df(self):
        csv_input = csv.reader(StringIO(self.response, newline=''), delimiter=';')
        rows = list(csv_input)
        data = rows[1:]
        columns = rows[0]
        df = pd.DataFrame(data, columns=columns)
        return df






class Transform_tge:

    def __init__(self, response, table):
        self.response = response
        self.table = table


    def get_headers(self):
        headers_list = []
        for element in self.table:
            headers = element.find_all('thead')[0].text
            headers = headers.strip().split('\n')
            clean_headers = [value for value in headers if value]
            header_1 = clean_headers[:3]
            index_name = clean_headers[3]
            header_2 = clean_headers[4:]
            headers_list.append((header_1, header_2, index_name))
        return headers_list



    def get_data(self):
        data_list = []
        for element in self.table:
            data = element.find_all('tbody')[0].text
            data = data.split('\n')
            cleaned_data = [value.strip() for value in data]
            cleaned_data_final = [value for value in cleaned_data if value]
            data_rows = []
            for i in range(0, len(cleaned_data_final), 7):
                row = cleaned_data_final[i : i + 7]
                data_rows.append(row)
            data_list.append(data_rows)
        return data_list



    def recreate_table(self, data, headers, date):
        df_list = []
        for data, headers, date in zip(data, headers, date):
            df = pd.DataFrame(data)
            df = df.set_index(0)
            header1 = []
            header2 = headers[1]
            for name in headers[0]:
                header1.extend([name, name])
                header = [header1, header2]
            df.columns = header
            index_name = headers[2]
            df.index.name = index_name 
            df = pd.concat([df], keys=[date], names=['Data'])
            df_list.append(df)      
        return pd.concat(df_list) 




    
