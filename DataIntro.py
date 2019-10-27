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

#TODO säädatan käsittely ja sen yhdistäminen leffadataan

#TODO: aika vertailu joka kääntää jokaisen kellonajan ja päivämäärän lähimpään tuntiin ja tekee 
#sen pohjalta vertauksen sen hetkisestä säästä

dates = []
dailyTotals = []
previousDay = datetime.date(2018, 1, 1)
total =  0
    
for index, row in df.iterrows():
#    print(df['Show Time'][index])
    if previousDay == df['Show Time'][index].date():
        total += df['Admissions'][index]
    else: 
        dates.append(previousDay)
        previousDay = df['Show Time'][index].date()
        dailyTotals.append(total)
        total = df['Admissions'][index]   
#Adding the final day as the iteration won't cover it:
dates.append(previousDay)
dailyTotals.append(total)

DTot = pd.DataFrame()
DTot['Date'] = dates
DTot['Attendances'] = dailyTotals
        
#TODO: suosituimmat päivät ja niide attribuutit

#Exploration
count = df.groupby('Event').count()
#Huomioita: Sama elokuva voi esiintyä usealla eri nimellä. Lisäksi vaihtelevasti elokuvien täsmennyksiä.
means = df.groupby('Event').mean() #pitää muuttaa tyypit oikein
