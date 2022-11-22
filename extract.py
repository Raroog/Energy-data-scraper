#!/usr/bin/env python


import pandas as pd
import requests
from io import StringIO
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from datetime import timedelta

class Extract:

    def __init__(self, raport, date1, date2):
        self.raport = raport
        self.date1 = date1
        self.date2 = date2

    def name_raport(self):
        if self.raport == 'tge':
            return self.raport
        elif self.raport == 'kse':
            return 'PL_WYK_KSE'
        else:
            return 'PL_GEN_MOC_JW_EPS'

    def transform_date(self, date_to_transform):
        if self.raport in ['kse', 'pse']:
            return datetime.strptime(date_to_transform, '%d-%m-%Y').strftime('%Y%m%d')
        else:
            return date_to_transform



    def generate_dates_for_tge(self):
        self.date1 = datetime.strptime(self.date1, '%d-%m-%Y').date()
        self.date2 = datetime.strptime(self.date2, '%d-%m-%Y').date()
        dates_df = pd.date_range(self.date1, self.date2 - timedelta(days=1), freq='d')
        dates_list = [date.strftime('%d-%m-%Y') for date in dates_df]
        return dates_list


    def generate_tge_url(self, dates_list):
        tge_urls = []
        for date in dates_list:
            tge_url = f'https://tge.pl/energia-elektryczna-rdn?dateShow={date}&dateAction='
            tge_urls.append(tge_url)
        return tge_urls



    def generate_pse_url(self, raport_name, tr_date1, tr_date2):
        return f"https://www.pse.pl/getcsv/-/export/csv/{raport_name}/data_od/{tr_date1}/data_do/{tr_date2}"



    def get_response(self, url, raport_name):
        if raport_name == 'tge':
            encoding = 'utf-8'
            response_list = []
            for element in url:
                reply = requests.get(element)
                reply.raise_for_status()
                reply.encoding = encoding
                response_list.append(reply.text)
            return response_list
        else:
            encoding = 'windows-1250'
            reply = requests.get(url)
            reply.raise_for_status()
            reply.encoding = encoding
            return reply.text




    def get_table_html(self, response):
        table_list = []
        for element in response:
            soup = BeautifulSoup(element, 'lxml')
            all_tables = soup.find_all('table')
            table = all_tables[2]
            table_list.append(table)
        return table_list


    

    


