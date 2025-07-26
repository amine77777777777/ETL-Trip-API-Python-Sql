
import pandas as pd
import requests
import json
import urllib
from utils import get_auth_headers, cif
from sqlalchemy import create_engine
import pyodbc

trip_df = pd.read_csv("trip_summaries.csv")
trip_details = []

for _, row in trip_df.iterrows():
    tripId = row["TripId"]
    plate = row["NumberPlate"]

    url_base = f"https://swjttodfapi021.jaltest.com/JaltestTelematicsAPI/json/trip/{tripId}"
    query = f"CIF={cif}&numberPlate={plate}"
    url = f"{url_base}?{query}"

    headers = get_auth_headers("GET", url_base, query)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        result = response.json().get("Result", {})
        result["TripId"] = tripId
        result["NumberPlate"] = plate
        trip_details.append(result)
    else:
        print(f"Error for TripId {tripId}: {response.status_code}")

trip_details_df = pd.DataFrame(trip_details)

# Normalize summaries
columns_to_flatten = ['BrakingSummary', 'ConsumptionSummary', 'EnergySummary', 'InertiaSummary', 'OrographySummary',
                      'RPMSummary', 'SpeedSummary', 'TimmeSummary', 'WeightSummary']
for col in columns_to_flatten:
    if col in trip_details_df:
        normalized = pd.json_normalize(trip_details_df[col])
        normalized.columns = [f"{col}_{c}" for c in normalized.columns]
        trip_details_df = pd.concat([trip_details_df.drop(columns=[col]), normalized], axis=1)

# Normalize Drivers
if "Drivers" in trip_details_df:
    drivers = pd.json_normalize(trip_details_df["Drivers"].explode())
    drivers.columns = [f"Drivers_{c}" for c in drivers.columns]
    trip_details_df = pd.concat([trip_details_df.drop(columns=["Drivers"]), drivers], axis=1)

# Drop unnecessary intervals
columns_to_drop = [
    'RPMSummary_RPMIntervals', 'SpeedSummary_SpeedIntervals'
]
trip_details_df.drop(columns=[col for col in columns_to_drop if col in trip_details_df], inplace=True)

# Save to SQL Server
db_str = "Driver={ODBC Driver 17 for SQL Server};Server=detassis\\DETASSIS_DWH;Database=POWERBI_DETASSIS;UID=sa;PWD=DeTass0939*"
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(db_str)}")

trip_details_df.to_sql("TripID_Jaltest_Agg", engine, if_exists="append", index=False)
print("Detailed trip data saved to SQL Server")
