from google.cloud import bigquery
import os

# Set credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./service_account.json"

client = bigquery.Client()
project_id = "de-zoomcamp-484115"
dataset_id = "trips_data_all"
tables = ["yellow_tripdata", "green_tripdata", "fhv_tripdata"]

print("BigQuery Table Record Counts:")
for table in tables:
    query = f"SELECT count(*) as count FROM `{project_id}.{dataset_id}.{table}`"
    try:
        query_job = client.query(query)
        results = query_job.result()
        for row in results:
            print(f"{table}: {row.count}")
    except Exception as e:
        print(f"Error querying {table}: {e}")
