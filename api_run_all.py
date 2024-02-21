# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 10:44:10 2024

@author: vcs-las
"""
import requests as req
import pandas as pd





def money_cost(lvl, base_cost):
    price = base_cost
    for i in range(lvl+1):
        price = (i+0.5)*base_cost*2+price
    return price

def resource_amount(lvl, base_cost):
    price = base_cost
    for i in range(lvl+1):
        price = (i+0.5)*base_cost*2+price
    return price

def production_rate(lvl):
    pass



key = '40bcfda00f3de0d721891079edcaa91b65cb952ce2736'


f = 1 #output type (0=csv, 1=json)
k = key
l = 'en' #lanugage
d = 30 #number of days


q = 1006 #query
url = f'https://www.resources-game.ch/resapi/?q={q}&f={f}&k={k}&l={l}&d={d}'
resp = req.get(url)
resultat = resp.json()
df_market_rates = pd.DataFrame(resultat)
df_market_rates = df_market_rates.apply(lambda col: pd.to_numeric(col, errors='ignore'))



q = 1002 #query
url = f'https://www.resources-game.ch/resapi/?q={q}&f={f}&k={k}&l={l}&d={d}'
resp = req.get(url)
resultat = resp.json()
df_production_rates = pd.DataFrame(resultat)
df_production_rates = df_production_rates.apply(lambda col: pd.to_numeric(col, errors='ignore'))



q = 1004 #query
url = f'https://www.resources-game.ch/resapi/?q={q}&f={f}&k={k}&l={l}&d={d}'
resp = req.get(url)
resultat = resp.json()
df_upgrades = pd.DataFrame(resultat)
df_upgrades  = df_upgrades .apply(lambda col: pd.to_numeric(col, errors='ignore'))



q = 1 #query
url = f'https://www.resources-game.ch/resapi/?q={q}&f={f}&k={k}&l={l}&d={d}'
resp = req.get(url)
resultat = resp.json()
df_my_factories = pd.DataFrame(resultat)
df_my_factories = df_my_factories.apply(lambda col: pd.to_numeric(col, errors='ignore'))




df = pd.merge(df_upgrades, df_my_factories, on='factoryID')


# Create a mask where 'price' is 0
mask = df_market_rates['price'] == 0
# Update 'price' where the mask is True with values from 'KIprice'
df_market_rates['price'][mask] = df_market_rates['KIprice'][mask]

#merged_df['price'] = money_cost(merged_df['lvl'], merged_df['baseUpgCost'])
df['price'] = df.apply(lambda row: money_cost(row['lvl'], row['baseUpgCost']), axis=1)
df['UpItemQty1'] = df.apply(lambda row: resource_amount(row['lvl'], row['baseUpgItemQty1']), axis=1)
df['UpItemQty2'] = df.apply(lambda row: resource_amount(row['lvl'], row['baseUpgItemQty2']), axis=1)
df['UpItemQty3'] = df.apply(lambda row: resource_amount(row['lvl'], row['baseUpgItemQty3']), axis=1)

#df['price_item1'] = df_market_rates[]
df['price_item1'] = df['baseUpgItemID1'].map(df_market_rates.set_index('itemID')['price'])
df['price_item2'] = df['baseUpgItemID2'].map(df_market_rates.set_index('itemID')['price'])
df['price_item3'] = df['baseUpgItemID3'].map(df_market_rates.set_index('itemID')['price'])


df.fillna(0, inplace=True)
df['total_price'] = df['price'] + df['UpItemQty1']*df['price_item1'] + df['UpItemQty2']*df['price_item2'] + df['UpItemQty3']*df['price_item3']


df['price_output'] = df['productID'].map(df_market_rates.set_index('itemID')['price'])
df['production'] = df['productID'].map(df_production_rates.set_index('itemID')['baseOutputPerHour'])*df['lvl']
df['production_value'] = df['production'] * df['price_output']


df_production_rates['fraction_credit'] = df_production_rates['creditsPerCycle']/df_production_rates['outputPerCycle']
df_production_rates['fraction1'] = df_production_rates['item1QtyPerCycle']/df_production_rates['outputPerCycle']
df_production_rates['fraction2'] = df_production_rates['item2QtyPerCycle']/df_production_rates['outputPerCycle']
df_production_rates['fraction3'] = df_production_rates['item3QtyPerCycle']/df_production_rates['outputPerCycle']



#df['payback'] = df['total_price']/df['production_value']
df['input_type1'] = df['factoryID'].map(df_production_rates.set_index('factoryID')['itemID1'])
df['input_type2'] = df['factoryID'].map(df_production_rates.set_index('factoryID')['itemID2'])
df['input_type3'] = df['factoryID'].map(df_production_rates.set_index('factoryID')['itemID3'])

df['credits_amount1'] = df['factoryID'].map(df_production_rates.set_index('factoryID')['fraction_credit'])*df['production']
df['input_amount1'] = df['factoryID'].map(df_production_rates.set_index('factoryID')['fraction1'])*df['production']
df['input_amount2'] = df['factoryID'].map(df_production_rates.set_index('factoryID')['fraction2'])*df['production']
df['input_amount3'] = df['factoryID'].map(df_production_rates.set_index('factoryID')['fraction3'])*df['production']


df['input_price1'] = df['input_type1'].map(df_market_rates.set_index('itemID')['price'])*df['input_amount1']
df['input_price2'] = df['input_type2'].map(df_market_rates.set_index('itemID')['price'])*df['input_amount1']
df['input_price3'] = df['input_type3'].map(df_market_rates.set_index('itemID')['price'])*df['input_amount1']

df.fillna(0, inplace=True)

df['expends'] = df['input_price1'] + df['input_price2'] + df['input_price3'] #+ df['credits_amount1']

df['profit'] = df['production_value'] - df['expends']
df['extra_profit'] = df['profit'] / df['lvl'] 

df['payback'] = df['total_price'] / df['extra_profit'] / 24

df_small = df[['factoryName', 'lvl', 'payback', 'total_price']]

df_small = df_small.sort_values(by='payback')
print(df_small)

df_small = df_small.reset_index()

for index, row in df.iterrows():
    print(f"Name: {row['factoryName']}, Score: {row['payback']:.1f}")
