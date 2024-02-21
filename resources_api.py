# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 10:44:10 2024

@author: vcs-las
"""
import requests as req
import pandas as pd

key = '40bcfda00f3de0d721891079edcaa91b65cb952ce2736'

q = 1001 #query
f = 1 #output type (0=csv, 1=json)
k = key
l = 'en' #lanugage
d = 30 #number of days

url = f'https://www.resources-game.ch/resapi/?q={q}&f={f}&k={k}&l={l}&d={d}'

resp = req.get(url)

resultat = resp.json()

df = pd.DataFrame(resultat)

df.to_csv('data/mine_data.csv')

