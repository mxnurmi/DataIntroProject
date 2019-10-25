#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 13:23:31 2019

@author: miska
"""

import numpy as np
import pandas as pd
import holidays 


df = pd.read_csv('show-list.csv', delimiter = ';', encoding='cp1252', 
                 usecols=[0, 1, 3, 4, 9, 10, 11, 12, 14, 18, 21])

df.rename(columns={'Unnamed: 1': 'Time'}, inplace=True)

weather = pd.read_csv('weather.csv', delimiter = ',')

#
df['Show Time'] = df['Show Time'].str.replace('Accounting Date: ', '')
df['Show Time'] = df[['Show Time']].fillna(method='ffill')
#df = df.dropna(subset=['Unnamed: 1'])
df = df.dropna(subset=['Event'])
df['Show Time'] = df['Show Time'].str.strip()
df['Show Time'] = pd.to_datetime(df['Show Time'] + ' ' + df['Time'])

df = df.astype({"Admissions": "int"})

#Holidays
fin_holidays = holidays.FI()
holiday = []
columns = list(df)

for i in df['Show Time']: 
    holiday.append(i in fin_holidays)
    
df.insert(2, "Holiday", holiday, True)




#TODO: aika vertilu joka kääntää jokaisen kellonajan ja päivämäärän lähimpään tuntiin ja tekee 
#sen pohjalta vertauksen sen hetkisestä säästä

#Exploration
print(df.groupby('Event').count())
#Huomioita: Sama elokuva voi esiintyä usealla eri nimellä. Lisäksi vaihtelevasti elokuvien täsmennyksiä.
means = df.groupby('Event').mean() #pitää muuttaa tyypit oikein
