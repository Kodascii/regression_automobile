import pandas as pd
import numpy as np
from currency_converter import CurrencyConverter



def graph_csv(df_full):
    
    df = df_full[['Name', 'Year', 'Fuel_Type', 'Price']]

    #split name and only keep the Brand
    df['Name'] = df['Name'].str.split(' ').str[0]


    #Add back Rover to Land
    def modify_text(text):
        old_text = 'Land'
        new_text = 'Land Rover'
        if old_text in text and new_text not in text:
            return text.replace(old_text, new_text)
        else:
            return text

    df['Name'] = df['Name'].apply(lambda x: modify_text(x))


    # convert from lakh to Indian Roupees to Euros
    cc = CurrencyConverter()
    lakh = 100000
    df['Price'] = df['Price'].apply(lambda x: x * lakh)
    df['Price'] = df['Price'].apply(lambda x: round(cc.convert(x, 'INR', 'EUR'), 2))
    
    #save new dataframe to a CSV file
    df.to_csv('clean_siteweb_CSV.csv', index=False)

def full_csv(df_full):
    
    df = df_full[['Name', 'Location', 'Year', 'Fuel_Type', 'Transmission', 'Owner_Type']].copy()

    df['Name'] = df['Name'].str.split(' ').str[0]
    
    def modify_text(text):
        old_text = 'Land'
        new_text = 'Land Rover'
        if old_text in text and new_text not in text:
            return text.replace(old_text, new_text)
        else:
            return text


    df.loc[:, 'Name'] = df['Name'].apply(lambda x: modify_text(x))
    
    print(df.head())
    
    df.to_csv('full_clean_siteweb_CSV.csv', index=False)

df_full = pd.read_csv('../../res/train.csv')

#csv pour les graphics
graph_csv(df_full)

#csv pour le formulaire
full_csv(df_full)


