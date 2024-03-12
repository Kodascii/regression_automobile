# Besoin pour clean_mileage_engine_power
import pandas as pd
import numpy as np

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
    

def clean_mileage_engine_power_(df):
    df['Mileage'] = df['Mileage'].apply(clean_mileage)
    df['Engine'] = df['Engine'].apply(clean_engine)
    df['Power'] = df['Power'].apply(clean_power)
    return df