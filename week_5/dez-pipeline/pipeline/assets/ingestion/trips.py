"""@bruin

name: ingestion.trips
type: python
image: python:3.11

connection: duckdb-default

materialization:
  type: table
  strategy: append

columns:
  - name: pickup_datetime
    type: timestamp
    description: "When the meter was engaged"
  - name: dropoff_datetime
    type: timestamp
    description: "When the meter was disengaged"
  - name: pickup_location_id
    type: integer
    description: "TLC Taxi Zone for pickup"
  - name: dropoff_location_id
    type: integer
    description: "TLC Taxi Zone for dropoff"
  - name: fare_amount
    type: float
    description: "The time-and-distance fare calculated by the meter"
  - name: payment_type
    type: integer
    description: "Numeric code signifying how the passenger paid"
  - name: taxi_type
    type: string
    description: "Type of taxi (yellow or green)"
  - name: extracted_at
    type: timestamp
    description: "Timestamp when the data was extracted"
@bruin"""

import os
import json
import pandas as pd
from datetime import datetime

def materialize():
    start_date = os.environ["BRUIN_START_DATE"]
    end_date = os.environ["BRUIN_END_DATE"]
    bruin_vars = json.loads(os.environ.get("BRUIN_VARS", "{}"))
    taxi_types = bruin_vars.get("taxi_types", ["yellow"])

    # Generate list of months between start and end dates
    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date)
    months = pd.date_range(start=start.replace(day=1), end=end, freq="MS")

    all_dfs = []
    base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data"

    for taxi_type in taxi_types:
        for month in months:
            year = month.year
            month_str = f"{month.month:02d}"
            url = f"{base_url}/{taxi_type}_tripdata_{year}-{month_str}.parquet"
            print(f"Fetching: {url}")
            try:
                df = pd.read_parquet(url)

                # Standardize column names for yellow vs green taxis
                col_mapping = {
                    "tpep_pickup_datetime": "pickup_datetime",
                    "tpep_dropoff_datetime": "dropoff_datetime",
                    "lpep_pickup_datetime": "pickup_datetime",
                    "lpep_dropoff_datetime": "dropoff_datetime",
                    "PULocationID": "pickup_location_id",
                    "DOLocationID": "dropoff_location_id",
                }
                df = df.rename(columns=col_mapping)

                # Select only the columns we need
                columns_to_keep = [
                    "pickup_datetime", "dropoff_datetime",
                    "pickup_location_id", "dropoff_location_id",
                    "fare_amount", "payment_type"
                ]
                df = df[[c for c in columns_to_keep if c in df.columns]]
                df["taxi_type"] = taxi_type
                df["extracted_at"] = datetime.now()

                all_dfs.append(df)
                print(f"  -> {len(df)} rows")
            except Exception as e:
                print(f"  -> Skipped: {e}")

    if not all_dfs:
        return pd.DataFrame()

    final_dataframe = pd.concat(all_dfs, ignore_index=True)
    print(f"Total rows: {len(final_dataframe)}")
    return final_dataframe
