from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="ecom_marketing_funnel_batch",
    start_date=datetime(2024, 1, 1),
    schedule="0 2 * * *",
    catchup=False,
    tags=["dezoomcamp", "ecommerce", "marketing", "batch"],
) as dag:
    ingest_to_gcs = BashOperator(
        task_id="ingest_to_gcs",
        bash_command=(
            "python /opt/airflow/dags/ingestion/ingest_olist_to_gcs.py "
            "--input-dir /opt/airflow/dags/data/raw "
            "--bucket ${GCS_BUCKET} "
            "--prefix raw/olist"
        ),
    )

    load_to_bq = BashOperator(
        task_id="load_to_bq",
        bash_command=(
            "python /opt/airflow/dags/ingestion/load_gcs_to_bq.py "
            "--project ${GCP_PROJECT_ID} "
            "--dataset ${BQ_DATASET_STAGING} "
            "--bucket ${GCS_BUCKET} "
            "--prefix raw/olist"
        ),
    )

    run_dbt = BashOperator(
        task_id="run_dbt",
        bash_command="cd /opt/airflow/dags/dbt && dbt run && dbt test",
    )

    ingest_to_gcs >> load_to_bq >> run_dbt
