#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 13:23:31 2019

@author: miska
"""

import numpy as np
import pandas as pd
import holidays 
import datetime


def replacer(dataColumn, *args):
    for i in args: 
        dataColumn = dataColumn.str.replace(i, '')
    return dataColumn

new = pd.read_csv('show-list.csv', delimiter = ';', encoding='cp1252', 
                 usecols=[0, 1, 3, 4, 9, 10, 11, 12, 14, 18, 21])

df = new.copy()

df.rename(columns={'Unnamed: 1': 'Time'}, inplace=True)

weather = pd.read_csv('weather.csv', delimiter = ',')

#
df['Show Time'] = df['Show Time'].str.replace('Accounting Date: ', '')
df['Show Time'] = df[['Show Time']].fillna(method='ffill')
df = df.dropna(subset=['Event'])
df['Show Time'] = df['Show Time'].str.strip()
df['Show Time'] = pd.to_datetime(df['Show Time'] + ' ' + df['Time'])

df = df.astype({'Admissions': 'int'})

df['Event'] = replacer(df['Event'], ')', '(', '2D', '3D', 'dub', 'orig', 'swe')
df['Event'] = df['Event'].str.rstrip()

#Holidays
fin_holidays = holidays.FI()
holiday = []
columns = list(df)

for i in df['Show Time']: 
    holiday.append(i in fin_holidays)
    
df.insert(1, "Holiday", holiday, True)


#TODO: aika vertailu joka kääntää jokaisen kellonajan ja päivämäärän lähimpään tuntiin ja tekee 
#sen pohjalta vertauksen sen hetkisestä säästä

dates = []
dailyTotals = []
previousDay = datetime.date(2018, 1, 1)
total =  0
for i,day in enumerate(df['Show Time'], start=1):
    print(day)
    while i not in df.index:
        i = i + 1
    print(df['Admissions'][i])
    if previousDay == day.date():
        total += df['Admissions'][i]
    else: 
        dates.append(previousDay)
        previousDay = day.date()
        dailyTotals.append(total)
        total = df['Admissions'][i]

#Exploration
count = df.groupby('Event').count()
#Huomioita: Sama elokuva voi esiintyä usealla eri nimellä. Lisäksi vaihtelevasti elokuvien täsmennyksiä.
means = df.groupby('Event').mean() #pitää muuttaa tyypit oikein
