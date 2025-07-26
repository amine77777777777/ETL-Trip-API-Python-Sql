
import requests
import json
import pandas as pd
from utils import get_auth_headers, cif

url = f"https://swjttodfapi021.jaltest.com/JaltestTelematicsAPI/json/vehicles?CIF={cif}"
headers = get_auth_headers("GET", "https://swjttodfapi021.jaltest.com/JaltestTelematicsAPI/json/vehicles", f"CIF={cif}")

response = requests.get(url, headers=headers, verify=False)
if response.status_code == 200:
    data = response.json()
    df = pd.json_normalize(data['Result'])
    df.to_csv("vehicles.csv", index=False)
    print("Vehicle list saved to vehicles.csv")
else:
    print(f"Error: {response.status_code} - {response.text}")
