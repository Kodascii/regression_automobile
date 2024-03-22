from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import pickle
from pydantic import BaseModel
import pandas as pd  # Import Pandas

class PredictionInput(BaseModel):
    Brand: str
    Location: str
    Year: int
    Fuel_Type: str
    Transmission: str
    Owner_Type: str
    Kilometers_Driven: float
    Mileage: float
    Engine: float
    Power: float
    Seats: int
    New_Price: int

app = FastAPI()

# Load the model
with open("../nettoyage/GBR.pkl", "rb") as model_file:
    model = pickle.load(model_file)

security = HTTPBearer()

def validate_token(http_auth: HTTPAuthorizationCredentials = Depends(security)):
    token_file = 'api_token.txt'
    
    with open(token_file, 'r') as file:
        token = file.read().strip()


    expected_token = token  # Replace with your actual token
    if http_auth.credentials != expected_token:
        raise HTTPException(status_code=403, detail="Invalid token")

@app.post("/predict/", dependencies=[Depends(validate_token)])
def predict(input_data: PredictionInput):
    print(input_data)
    # Convert the Pydantic model to a dictionary
    input_dict = input_data.dict()
    
    # Convert the dictionary to a Pandas DataFrame
    # Note: The input is wrapped in a list to create a single-row DataFrame
    df = pd.DataFrame([input_dict])

    # Make a prediction using the DataFrame
    prediction = model.predict(df)
    return {"prediction": prediction.tolist()}
