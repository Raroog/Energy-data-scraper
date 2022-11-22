#!/usr/bin/env python

import pandas as pd


class Load:

    def __init__(self, raport, df, date1, date2=None):
        self.raport = raport
        self.df = df
        self.date1 = date1
        self.date2 = date2


    def load_csv_locally(self):
        self.df.to_csv(f'{self.raport}_{self.date1}_{self.date2}.csv')
        print(f'wygenerowano plik: {self.raport}_{self.date1}_{self.date2}.csv')

