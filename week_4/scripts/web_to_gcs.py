import os
import requests
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from google.cloud import storage
from google.cloud import bigquery

# --- Constants ---
BUCKET = "taxi-all-data"
PROJECT_ID = "de-zoomcamp-484115"
DATASET = "trips_data_all"
CREDENTIALS_FILE = "./service_account.json"
DOWNLOAD_DIR = "./downloads"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_FILE

def download_file(url, local_path):
    """Downloads a file from url to local_path."""
    if os.path.exists(local_path):
        print(f"File already exists: {local_path}")
        return True

    try:
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        print(f"Downloading: {url}")
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {local_path}")
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def standardize_schema(local_path):
    """Reads parquet file, fixes schema (ehail_fee), and returns path to fixed file."""
    try:
        print(f"Standardizing schema for: {local_path}")
        df = pd.read_parquet(local_path)
        
        # schema fixes
        if 'ehail_fee' in df.columns:
            df['ehail_fee'] = df['ehail_fee'].astype(float)
        
        # Write back to parquet using pyarrow engine to ensure compatibility
        df.to_parquet(local_path, engine='pyarrow')
        print(f"Schema standardized: {local_path}")
        return local_path
    except Exception as e:
        print(f"Error standardizing schema for {local_path}: {e}")
        return None

def upload_to_gcs(bucket_name, object_name, local_file):
    """Uploads a file to the bucket."""
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(object_name)
        blob.upload_from_filename(local_file)
        print(f"GCS: {object_name} uploaded.")
        return True
    except Exception as e:
        print(f"Failed to upload {object_name}: {e}")
        return False

def load_to_bigquery(uri, service):
    """Loads data from GCS to BigQuery."""
    try:
        client = bigquery.Client()
        table_id = f"{PROJECT_ID}.{DATASET}.{service}_tripdata"

        job_config = bigquery.LoadJobConfig(
            autodetect=True,
            source_format=bigquery.SourceFormat.PARQUET,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
            schema_update_options=[bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION],
        )

        load_job = client.load_table_from_uri(
            uri, table_id, job_config=job_config
        )

        print(f"BigQuery: Loading {uri} into {table_id}...")
        load_job.result()  # Waits for the job to complete.
        print(f"BigQuery: Job finished. Table {table_id} now has {load_job.output_rows} rows.")
        return True
    except Exception as bq_error:
        print(f"BigQuery Error for {uri}: {bq_error}")
        return False

def main():
    # Define services and years to process
    services = {
        'yellow': ['2019', '2020'],
        'green': ['2019', '2020'],
        'fhv': ['2019']
    }
    
    # Phase 1: Download
    files_to_process = []
    print("--- Phase 1: Download ---")
    for service, years in services.items():
        for year in years:
            for i in range(1, 13):
                month = f"{i:02d}"
                file_name = f"{service}_tripdata_{year}-{month}.parquet"
                request_url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{file_name}"
                local_path = os.path.join(DOWNLOAD_DIR, service, file_name)
                
                if download_file(request_url, local_path):
                    files_to_process.append((service, local_path, file_name))
                else:
                    print(f"Skipping {file_name} due to download failure.")

    # Phase 2: Process, Upload, Load
    print("\n--- Phase 2: Process, Upload, Load ---")
    for service, local_path, file_name in files_to_process:
        print(f"\nProcessing: {file_name}")
        
        # 1. Standardize Schema
        fixed_path = standardize_schema(local_path)
        if not fixed_path:
            continue
            
        # 2. Upload to GCS
        object_name = f"{service}/{file_name}"
        if upload_to_gcs(BUCKET, object_name, fixed_path):
            
            # 3. Load to BigQuery
            gcs_uri = f"gs://{BUCKET}/{object_name}"
            load_to_bigquery(gcs_uri, service)

if __name__ == "__main__":
    main()