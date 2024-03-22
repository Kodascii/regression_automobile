import pandas as pd
import pickle

from typing import Annotated
from pydantic import BaseModel

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


# Fictitious database
users_db = {
    "root": {
        'username': "root",
        'hashed_password': 'fakehashed_123',
        'disabled': False
    }
}


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
gbr = pickle.load(open('models/GBR.pkl', 'rb'))


class User(BaseModel):
    username: str
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

class VehicleModel(BaseModel):
    brand             : str
    location          : str
    year              : int
    kilometers_driven : int
    fuel_type         : str
    transmission      : str
    owner_type        : str
    mileage           : float
    engine            : int
    power             : float
    new_price         : int


def vehicle_model2df(data:VehicleModel):
    """
    Converts `VehicleModel` data, into a `DataFrame`.
    """
    
    data = {
        'Brand'             : [data.brand],
        'Location'          : [data.location],
        'Year'              : [data.year],
        'Kilometers_Driven' : [data.kilometers_driven],
        'Fuel_Type'         : [data.fuel_type],
        'Transmission'      : [data.transmission],
        'Owner_Type'        : [data.owner_type],
        'Mileage'           : [data.mileage],
        'Engine'            : [data.engine],
        'Power'             : [data.power],
        'New_Price'         : [data.new_price]
    }

    return pd.DataFrame(data)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def fake_hash_password(password: str):
    return "fakehashed_" + password

def fake_decode_token(token):
    user = get_user(users_db, token)
    return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Endpoint to authenticate users and generate access tokens.

    Returns:
    - JSON response containing an access token if authentication is successful.

    Raises:
    - HTTPException(400): If incorrect username or password is provided.
    """

    user_dict = users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

@app.post('/prediction')
async def predict(data:VehicleModel, token: str = Depends(oauth2_scheme)):
    """
    Predicts the price of a vehicle with the GradiantBoostingRegressor model, based on provided features.
    """

    prediction = gbr.predict(vehicle_model2df(data))[0]
    return { 'predicted_price': prediction }