from google.cloud import bigquery
import os

# Set credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./service_account.json"

client = bigquery.Client()
project = "de-zoomcamp-484115"
dataset = "trips_data_all"
table = "yellow_tripdata"

try:
    t = client.get_table(f"{project}.{dataset}.{table}")
    print(f"Columns in {table}:")
    for s in t.schema:
        print(f"{s.name}: {s.field_type}")
except Exception as e:
    print(f"Error getting table {table}: {e}")
