# Besoin pour clean_mileage_engine_power
import pandas as pd
import numpy as np


data_train = pd.read_csv('../res/train.csv')
data_test = pd.read_csv('../res/test.csv')
default_info2del = ['(diesel)', '(petrol)', '(at)', 'diesel', 'petrol', 'at', 'tdi', 'mt']

def format_brand_name(str):
    if str == 'Land':
        return 'Land Rover'
    if str.capitalize() == 'Isuzu':
        return 'Isuzu'
    
    return str

def split_name(df):
    df.insert(1, 'Model', '')

    for index in df.index:
        name = df.at[index, 'Name']
        ws_idx = name.find(' ')
        brand = format_brand_name(name[:ws_idx])
        model = name[ws_idx+1:]

        df.at[index, 'Name'] = brand
        df.at[index, 'Model'] = model

    df.rename(columns={'Name': 'Brand'}, inplace=True)
    return df

def calc_words_occ(df):
    builder = []   # [(W_1, N_1), (W_2, N_2), ..., (W_m, N_m)]

    # Looping through the rows of a dataframe column
    for index in df.index:              
        words = df.at[index]
        splitted = words.split(' ')
        
        for word in splitted:
            found = False

            # Check if the 'word' is in the first element of any tuple in 'word_occurences' list
            for i, tup in enumerate(builder):
                if word.lower() == tup[0].lower():
                    builder[i] = (tup[0], tup[1] + 1)
                    found = True
                    break

            if not found:
                builder.append((word, 1))

    return builder

def split_desired_unrelated(words_occ, count, default_unrelated=[]):
    builder = { 'desired': [], 'unrelated': [] }
    
    for word, occ in words_occ:
        if occ <= count or word.lower() in default_unrelated:
            builder['unrelated'].append(word)
        else:
            builder['desired'].append(word)

    return builder

def desired_index(word, desired_unrelated):
    desired_lower = [ x.lower() for x in desired_unrelated['desired']]
    word_lower = word.lower()
    if word_lower in desired_lower:
        return desired_lower.index(word_lower)
    else:
        return -1
    
def clean_model(df, desired_unrelated):
    for index in df.index:
        model = df.at[index, 'Model']
        words = model.split(' ')
        builder = []

        for word in words:
            word_index = desired_index(word, desired_unrelated)
            if word_index != -1:
                builder.append(desired_unrelated['desired'][word_index])

        builder.sort()
        df.at[index, 'Model'] = ' '.join(builder)

    return df

def clean_mileage(mileage):
    if pd.isna(mileage):  # Gérer les valeurs NaN
        return np.nan
    num, unit = mileage.split(' ')[0], mileage.split(' ')[1]
    num = float(num)
    if unit == 'km/kg':
        return num * 1.40
    elif unit == 'kmpl':
        return num
    else:
        return np.nan
    
def clean_engine(engine):
    if pd.isna(engine):
        return np.nan
    num, unit = engine.split(' ')[0], engine.split(' ')[1]
    num = float(num)
    if unit == 'CC':
        return num
    
def clean_power(power):
    if pd.isna(power) or power.split(' ')[0].lower() == 'null':
        return np.nan
    num, unit = power.split(' ')[0], power.split(' ')[1]
    try:
        num = float(num)
        if unit == 'bhp':
            return num
    except ValueError:
        return np.nan
    
def clean_new_price(new_price):
    if pd.isnull(new_price):
        return 0
    return 1

def clean_price(price):
    if pd.isna(price):
        return np.nan
    return price * 1104.05

def fillnans(df, cols):
    for col in cols:
        if col == 'Seats':
            df[cols] = df[cols].fillna(df[cols].median())
        else:
            df[col] = df[col].fillna(df[col].mode()[0])
    return df

def drop_outliers(df, on_column:str):
    # Calcul de la moyenne
    mean_price = df[on_column].mean()
    # Calcul de l'écart-type
    std_price = df[on_column].std()
    # Calcul du Z-score pour chaque observation dans la colonne 'Price'
    z_score = (df[on_column] - mean_price) / std_price
    # Supprimer les lignes contenant des valeurs aberrantes
    return df[abs(z_score) <= 3]


def clean_df(df):
    df = split_name(df.copy())
    df.drop('Model', axis=1, inplace=True)
    df.drop(columns=['Seats'], axis=1, inplace=True)
    #words_occ = calc_words_occ(df['Model'])
    #words_occ = split_desired_unrelated(words_occ, unrelated_occ, default_info2del)
    #df = clean_model(df, words_occ)

    df['Mileage'] = df['Mileage'].apply(clean_mileage)
    df['Engine'] = df['Engine'].apply(clean_engine)
    df['Power'] = df['Power'].apply(clean_power)
    df['New_Price'] = df['New_Price'].apply(clean_new_price)
    # if target: df['Price'] = df['Price'].apply(clean_price)
    fillnans(df, ['Mileage', 'Engine', 'Power'])
    df = drop_outliers(df, 'Kilometers_Driven')
    df = drop_outliers(df, 'Mileage')
    df = drop_outliers(df, 'Engine')
    df = drop_outliers(df, 'Power')
    df = drop_outliers(df, 'Price')

    return df

# clean_train = clean_csv(data_train)
# clean_train.to_csv('clean_train.csv', index=False)