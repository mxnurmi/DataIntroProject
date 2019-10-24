#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 13:23:31 2019

@author: miska
"""

import numpy as np
import pandas as pd


df = pd.read_csv('show-list.csv', delimiter = ';', encoding='cp1252', usecols=[0, 1, 3, 4, 9, 10, 11, 12, 14, 18, 21])

#
df['Show Time'] = df['Show Time'].str.replace('Accounting Date: ', '')
df['Show Time'] = df[['Show Time']].fillna(method='ffill')
df = df.dropna(subset=['Unnamed: 1'])
df['Show Time'] = df['Show Time'].str.strip()
df['Show Time']=pd.to_datetime(df['Show Time'])


#TODO: Poista tyhjät sekä turhat palkit.Tärkeitä palkkeja ainakin alkuaika, admissions, 3D vai ei distributor, ja tyyppi

#Exploration
print(df.groupby('Event').count())
#Huomioita: Sama elokuva voi esiintyä usealla eri nimellä. Lisäksi vaihtelevasti elokuvien täsmennyksiä.
means = df.groupby('Event').mean() #pitää muuttaa tyypit oikein
