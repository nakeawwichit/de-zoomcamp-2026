from google.cloud import bigquery
import os

# Set credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./service_account.json"

client = bigquery.Client()
dataset_id = "trips_data_all"
project_id = "de-zoomcamp-484115"
tables = ["yellow_tripdata", "green_tripdata", "fhv_tripdata"]

for table in tables:
    table_ref = f"{project_id}.{dataset_id}.{table}"
    try:
        client.delete_table(table_ref, not_found_ok=True)
        print(f"Dropped table {table_ref}")
    except Exception as e:
        print(f"Error dropping {table_ref}: {e}")
