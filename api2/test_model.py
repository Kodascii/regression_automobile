import pickle

with open("../nettoyage/GBR.pkl", "rb") as model_file:
    model = pickle.load(model_file)
    

Brand='Maruti'
Location='Mumbai'
Year=2010 Fuel_Type='CNG' 
Transmission='Manual' 
Owner_Type='First' 
Kilometers_Driven=75000.0 
Mileage=15.0 Engine=1000.0 
Power=70.0 Seats=5 
New_Price=0