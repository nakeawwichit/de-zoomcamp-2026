import argparse

from google.cloud import bigquery


TABLE_MAP = {
    "olist_orders_dataset.parquet": "stg_olist_orders_raw",
    "olist_order_items_dataset.parquet": "stg_olist_order_items_raw",
    "olist_products_dataset.parquet": "stg_olist_products_raw",
    "product_category_name_translation.parquet": "stg_category_translation_raw",
}


def load_parquet_table(
    client: bigquery.Client, project: str, dataset: str, bucket: str, prefix: str, file_name: str, table_name: str
) -> None:
    table_id = f"{project}.{dataset}.{table_name}"
    uri = f"gs://{bucket}/{prefix}/{file_name}"
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )
    load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
    load_job.result()
    table = client.get_table(table_id)
    print(f"Loaded {uri} -> {table_id} ({table.num_rows} rows)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Load Olist parquet files from GCS into BigQuery staging")
    parser.add_argument("--project", required=True, help="GCP project id")
    parser.add_argument("--dataset", required=True, help="BigQuery dataset for staging")
    parser.add_argument("--bucket", required=True, help="GCS bucket name")
    parser.add_argument("--prefix", default="raw/olist", help="GCS prefix")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    client = bigquery.Client(project=args.project)
    for file_name, table_name in TABLE_MAP.items():
        load_parquet_table(
            client=client,
            project=args.project,
            dataset=args.dataset,
            bucket=args.bucket,
            prefix=args.prefix,
            file_name=file_name,
            table_name=table_name,
        )


if __name__ == "__main__":
    main()
