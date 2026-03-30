import argparse
from pathlib import Path

import pandas as pd
from google.cloud import storage


FILES = [
    "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_products_dataset.csv",
    "product_category_name_translation.csv",
]


def upload_dataframe_as_parquet(
    client: storage.Client, bucket_name: str, blob_name: str, dataframe: pd.DataFrame
) -> None:
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    parquet_bytes = dataframe.to_parquet(index=False)
    blob.upload_from_string(parquet_bytes, content_type="application/octet-stream")


def ingest(input_dir: Path, bucket: str, prefix: str) -> None:
    client = storage.Client()
    for file_name in FILES:
        file_path = input_dir / file_name
        if not file_path.exists():
            raise FileNotFoundError(f"Missing input file: {file_path}")

        dataframe = pd.read_csv(file_path)
        rows = len(dataframe.index)
        blob_name = f"{prefix}/{file_name.replace('.csv', '.parquet')}"
        upload_dataframe_as_parquet(client, bucket, blob_name, dataframe)
        print(f"Uploaded {file_name} ({rows} rows) to gs://{bucket}/{blob_name}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest Olist CSV files to GCS parquet")
    parser.add_argument("--input-dir", required=True, type=Path, help="Directory with raw CSV files")
    parser.add_argument("--bucket", required=True, help="Target GCS bucket")
    parser.add_argument("--prefix", default="raw/olist", help="Target GCS prefix")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    ingest(args.input_dir, args.bucket, args.prefix)
