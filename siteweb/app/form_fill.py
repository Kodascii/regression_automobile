import pandas as pd
import numpy as np

def fill_form():
    csv_file = 'full_clean_siteweb_CSV.csv'
    df = pd.read_csv(csv_file)
    
    column_names = {'Name':[], 'Location':[], 'Year':[], 'Fuel_Type':[], 'Transmission':[], 'Owner_Type':[]}
    
    for column in column_names.keys():
        unique_elements = df[column].unique().tolist()
        column_names[column] = sorted(unique_elements, key=lambda x: (isinstance(x, str), x))
        
    return column_names
    
fill_form()
    