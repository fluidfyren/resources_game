import pandas as pd
import os

def list_files_sorted(folder_path):
    """
    List all files in the specified folder, sorted alphabetically.
    
    Args:
    folder_path (str): The path to the folder from which to list files.
    
    Returns:
    list: A list of file names, sorted alphabetically.
    """
    # List all items in the folder
    items = os.listdir(folder_path)
    
    # Filter out directories, keeping only files
    files = [item for item in items if os.path.isfile(os.path.join(folder_path, item))]
    
    # Sort the list of files alphabetically
    files_sorted = sorted(files)
    
    return files_sorted


def add_price_columns(dataframes):
    for i, df in enumerate(dataframes[1:], start=1):
    # Add the 'price' column from each DataFrame to the first DataFrame
    # Naming the new column as 'price_i' where i is the index in the list
        dataframes[0][f'price_{i}'] = df['price']
    return dataframes[0]


if __name__ == "__main__":
    folder = 'market_rates'
    files = list_files_sorted(folder)
    
    old_files = []
    for file in files[:-1]:
        df = pd.read_csv(f'{folder}/{file}')
        mask = df['price'] == 0
        df['price'][mask] = df['KIprice'][mask]
        old_files.append(df)
    
    combined_dataframe = add_price_columns(old_files)
    
    combined_dataframe = combined_dataframe.drop('KIprice', axis=1)
    price_columns = [col for col in combined_dataframe.columns if 'price' in col]
    combined_dataframe['avg_price'] = combined_dataframe[price_columns].mean(axis=1)
    #df_market_rates['factor'] = df_market_rates['price']/df_market_rates['KIprice']

    df_new = pd.read_csv(f'{folder}/{files[-1]}')
    
    mask = df_new['price'] == 0
    df_new['price'][mask] = df_new['KIprice'][mask]
    
    df_new['trade_ratio'] = df_new['price']/combined_dataframe['avg_price']
    
    df_small = df_new[['itemName','trade_ratio']]
    
    df_small = df_small.sort_values(by='trade_ratio', ascending=False)
    print(df_small)







