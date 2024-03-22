import requests

url = "http://127.0.0.1:8000/token"
# Connection vers l'API
response = requests.post(url, data={'username': 'root', 'password': '123'})

if response.status_code == 200:
    # Saisi du token
    token = response.json().get('access_token')
    # URL de prediction
    prediction_url = "http://127.0.0.1:8000/prediction"
    # En-têtes qui portent le token
    headers = {"Authorization": f"Bearer {token}"}

    # Example de prediction:
    example_vehicle = {
        'brand'             : 'Maruti',
        'location'          : 'Mumbai',
        'year'              : 2010,
        'kilometers_driven' : 72000,
        'fuel_type'         : 'CNG',
        'transmission'      : 'Manual',
        'owner_type'        : 'First',
        'mileage'           : 26.6,
        'engine'            : 998,
        'power'             : 58.16,
        'new_price'         : 0
    }

    prediction_response = requests.post(prediction_url, headers=headers, json=example_vehicle)

    if prediction_response.status_code == 200:
        print("Data:", prediction_response.json())
    else:
        print("Error:", prediction_response.status_code)
else:
    print("Error:", response.status_code)