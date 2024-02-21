import pandas as pd


def money_cost(lvl, base_cost):
    price = base_cost
    for i in range(lvl+1):
        price = (i+0.5)*base_cost*2+price
        print(price)
    return price

def resource_amount(lvl, base_cost):
    price = base_cost
    for i in range(lvl+1):
        price = (i+0.5)*base_cost*2+price
        print(price)
    return price



df_market_rates = pd.read_csv('market_rates/market_rates_20240218.csv')

df_production_rates = pd.read_csv('data/production_rates.csv')
df_upgrades = pd.read_csv('data/factory_upgrade_data.csv')
df_my_factories = pd.read_csv('data/my_factories.csv')

df = pd.merge(df_upgrades, df_my_factories, on='factoryID')

#df_market_rates['price'] = df_market_rates['KIprice']

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







