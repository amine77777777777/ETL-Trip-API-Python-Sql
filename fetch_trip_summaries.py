import pandas as pd
import requests
import json
from datetime import datetime, timezone
from utils import get_auth_headers, cif

# Read number plates
vehicles_df = pd.read_csv("vehicles.csv")
number_plates = vehicles_df["NumberPlate"].dropna().tolist()

# Handle dates
last_file = "TripIdJaltest_Agg.txt"
def get_last_processed():
    if not pd.io.common.file_exists(last_file):
        return "2025-01-01T00:00:00"
    with open(last_file, 'r') as f:
        return f.read().strip()

def update_last_processed(new_date):
    with open(last_file, 'w') as f:
        f.write(new_date)

last_date = get_last_processed()
now_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

url_base = "https://swjttodfapi021.jaltest.com/JaltestTelematicsAPI/json/trips"
all_trips = []

for plate in number_plates:
    query = f"CIF={cif}&numberPlate={plate}&startDate={last_date}&endDate={now_date}&languageCode=en"
    url = f"{url_base}?{query}"
    headers = get_auth_headers("GET", url_base, query)

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json().get("Result", [])
        for trip in result:
            trip["NumberPlate"] = plate
        all_trips.extend(result)
    else:
        print(f"Error for {plate}: {response.status_code}")

df = pd.DataFrame(all_trips)
df.to_csv("trip_summaries.csv", index=False)
update_last_processed(now_date)
print("Trip summaries saved to trip_summaries.csv")