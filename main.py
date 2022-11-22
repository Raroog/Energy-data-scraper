#!/usr/bin/env python

#pip install python-dateutil

import argparse
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
import extract
import transform
import load


print('Wpisz pse jeśli chcesz otrzymać raport: Praca KSE- Generacja mocy Jednostek Wytwórczych')
print('Wpisz kse jeśli chcesz otrzymać raport: Praca KSE - wielkości podstawowe')
print('Wpisz tge jeśli chcesz otrzymać raport: Rynek Dnia Następnego - raporty godzinowe')
print('tabela tge dostępna tylko dla ostatnich 3 miesięcy')
print('Wpisz pierwszą datę w formacie DD-MM-YYYY')
print('Jeśli chcesz dane z przedziału czasowego wpisz drugą datę w formacie DD-MM-YYYY')

parser = argparse.ArgumentParser(description='Get User Input')
parser.add_argument('--date1', required=True, help='First Date of a Range')
parser.add_argument('--date2', required=True, help='Second Date of a Range')
parser.add_argument('--raport', required=True, help='Name of the Raport')
args = parser.parse_args()


date1 = args.date1
date2 = args.date2
raport = args.raport.lower()

d1 = datetime.strptime(date1, "%d-%m-%Y")
d2 = datetime.strptime(date2, "%d-%m-%Y")

if d1 > d2:
    temp = date1
    date1 = date2 
    date2 = temp



def check_raport(raport):
    if raport in ['tge', 'kse', 'pse']:
        print('OK')
    else:
        raise Exception(f"The given raport name: {raport} is not correct")



def check_date(date_to_transform):
    try:
        datetime.strptime(date_to_transform, '%d-%m-%Y')
        if datetime.strptime(date_to_transform, '%d-%m-%Y').date() <= date.today():
            print('OK')
        else:
            raise Exception(f"The given date: {date_to_transform} can't be future date")
    except ValueError:
        raise Exception(f"The given date: {date_to_transform} is not in correct format")


def check_tge_date(date_to_check):
    minimum_date = date.today() + relativedelta(months=-3)
    date_to_compare = datetime.strptime(date_to_check, '%d-%m-%Y').date()
    if minimum_date <= date_to_compare:
        print('OK')
    else:
        raise Exception(f"The given date: {date_to_check} for tge raport can't be more than 3 months from now")


if __name__ == '__main__':

#CHECK USER INPUT
#ALL

#Sprawdza czy nazwa raportu jest OK
    check_raport(raport)

#Sprawdza czy data(y) jest w poprawnym formacie
    check_date(date1)
    check_date(date2)

#TGE        
#Sprawdza czy data(y) dla tge nie jest więcej niż 3 miesiące wstecz
    if raport == 'tge':
        check_tge_date(date1)
        check_tge_date(date2)


#EXTRACT

    extraction = extract.Extract(raport, date1, date2)

#ALL
#Zmienia nazwę raportu na pasującą do URL
    raport_name = extraction.name_raport()

#Zmienia format daty w zależności od raportu
    date1 = extraction.transform_date(date1)
    date2 = extraction.transform_date(date2)

#TGE
#Generuje listę dat jeśli raport to tge z przediału czasu
    if raport_name == 'tge':
        dates = extraction.generate_dates_for_tge()

#Generuje url(e)
        url = extraction.generate_tge_url(dates)


#PSE i KSE
#Generuje url(e)
    else:
        url = extraction.generate_pse_url(raport_name, date1, date2)


#ALL
#Generuje odpowiedź do zapytania
    response = extraction.get_response(url, raport_name)

#TGE
#Generuje html z tabeli dla raportu tge
    if raport_name == 'tge':
        table_html = extraction.get_table_html(response)


#TRANSFORM
#PSE i KSE
    transform_pse_or_kse = transform.Transform_kse_or_pse(response)


#KSE
#Generuje DataFrame z raportem
    if raport == 'kse':
        final_kse_df = transform_pse_or_kse.pse_or_kse_to_df()
        final_df = final_kse_df


#PSE
#Generuje DataFrame z raportem
    if raport == 'pse':
        pse_df = transform_pse_or_kse.pse_or_kse_to_df()

        transform_pse = transform.Transform_pse(pse_df)

#Transformuje datę i czas w raporcie
        pse_df = transform_pse.transform_date_time_pse()
        final_pse_df = transform_pse.transform_unpivot_hours_pse(pse_df)
        final_df = final_pse_df


#TGE
    if raport == 'tge':
        transform_tge = transform.Transform_tge(response, table_html)

#Bierze nazwy kolumn z tabeli
        headers = transform_tge.get_headers()

#Bierze dane z tabeli    
        data_rows = transform_tge.get_data()

#Odtwarza tabelę w DataFrame
        final_tge_df = transform_tge.recreate_table(data_rows, headers, dates)
        final_df = final_tge_df


#LOAD
#ALL
    load_csv = load.Load(raport, final_df, date1, date2)

#Generuje plik CSV lokalnie
    load_csv.load_csv_locally()


    












    
            



