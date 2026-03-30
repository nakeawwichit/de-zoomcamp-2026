# E-commerce Marketing Funnel (GCP Batch + Streamlit)

End-to-end batch data pipeline on GCP for retail marketing analysis using the
Brazilian E-Commerce Public Dataset by Olist.

## Problem statement

Marketing and category teams need a reliable daily view of:

1. Which product categories drive orders and revenue
2. How order lifecycle conversion changes over time

Without a standardized pipeline, these metrics are fragmented and hard to
reproduce.

## Dataset

- Source: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- Scope used in this project:
  - `olist_orders_dataset.csv`
  - `olist_order_items_dataset.csv`
  - `olist_products_dataset.csv`
  - `product_category_name_translation.csv`

## Funnel definition

This project uses an order-lifecycle funnel (order-centric):

- `placed`: order has `order_purchase_timestamp`
- `approved`: order has `order_approved_at`
- `delivered`: order has `order_delivered_customer_date`

Note: this is not a web event funnel (`view -> cart -> purchase`).

## Architecture

1. Batch ingestion reads local raw CSV files and writes parquet files to GCS raw zone
2. BigQuery external load creates staging tables from raw files
3. dbt builds marts optimized for dashboard queries
4. Streamlit reads BigQuery marts and renders two dashboard tiles

## Project structure

- `ingestion/`: batch ingestion and BigQuery loading scripts
- `orchestration/`: Airflow DAG for end-to-end batch run
- `dbt/`: staging and mart models with tests
- `dashboard/`: Streamlit app
- `terraform/`: GCP infrastructure (GCS, BigQuery datasets, IAM)

## Prerequisites

- Python 3.10+
- GCP project with billing enabled
- `gcloud` authenticated (`gcloud auth application-default login`)
- Terraform 1.5+
- dbt-bigquery

## Environment variables

Create `.env` from the template:

```bash
cp .env.example .env
```

Required variables:

- `GCP_PROJECT_ID`
- `GCP_REGION`
- `GCS_BUCKET`
- `BQ_DATASET_STAGING`
- `BQ_DATASET_MART`
- `GOOGLE_APPLICATION_CREDENTIALS` — path to a service account JSON with BigQuery access (recommended: `./service_account.json` in this folder). Optional if you use Application Default Credentials from `gcloud auth application-default login` only; in that case remove or comment out this line.

## Run dashboard only (local)

Use this when BigQuery marts are already built (`mart_category_daily_performance`, `mart_order_lifecycle_funnel_daily` in the mart dataset).

1. Put your GCP service account key file in this directory as `service_account.json` (or set `GOOGLE_APPLICATION_CREDENTIALS` in `.env` to the correct path).

2. From the **project root** (`ecommerce-marketing-funnel`):

```bash
cp .env.example .env
# Edit .env: set GCP_PROJECT_ID, BQ_DATASET_MART, and GOOGLE_APPLICATION_CREDENTIALS if needed

set -a && source .env && set +a
cd dashboard
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

3. Open the URL shown in the terminal (usually [http://localhost:8501](http://localhost:8501)).

The app needs `GCP_PROJECT_ID` and `BQ_DATASET_MART` in the environment (loaded from `.env` via `source` above).

**Tip:** The Olist public dataset is mostly **2016–2018**. If you pick a date range outside that span, charts will show no data. The sidebar shows the min/max dates available in your mart tables.

## Deploy dashboard (Cloud Run — for homework / peer review)

Deploy a **public HTTPS URL** so peers can open the dashboard without your laptop.

**Requirements**

- `gcloud` installed and logged in (`gcloud auth login` and `gcloud auth application-default login` as needed)
- Terraform already applied so the pipeline service account exists (default: `ecom-funnel-pipeline@<PROJECT>.iam.gserviceaccount.com`) with BigQuery access
- BigQuery marts already built (`dbt run` completed)

**One-command deploy** (from project root, uses `.env`):

```bash
chmod +x scripts/deploy_cloud_run.sh
./scripts/deploy_cloud_run.sh
```

The script enables required APIs, builds the container from [`dashboard/Dockerfile`](dashboard/Dockerfile), deploys to Cloud Run, sets `GCP_PROJECT_ID` and `BQ_DATASET_MART`, and prints the service URL.

**Environment overrides (optional)**

| Variable | Default | Meaning |
|----------|---------|---------|
| `CLOUD_RUN_SERVICE` | `ecom-marketing-dashboard` | Cloud Run service name |
| `CLOUD_RUN_SERVICE_ACCOUNT` | `ecom-funnel-pipeline@...` | Runtime SA (must query BigQuery) |

**After deploy:** Copy the printed URL into your homework README / submission form. The app uses the **service account identity on Cloud Run** (not `service_account.json` on disk), so peers only need the link.

**If build fails:** Ensure Cloud Build has permission to deploy (project Editor, or grant the Cloud Build SA the Cloud Run Admin role). First deploy can take several minutes.

## How to run (full pipeline)

### 1) Provision infrastructure

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform apply -var-file=terraform.tfvars
```

### 2) Install python dependencies

```bash
cd ../ingestion
pip install -r requirements.txt
```

### 3) Ingest raw files to GCS and load BigQuery staging

```bash
python ingest_olist_to_gcs.py \
  --input-dir ../data/raw \
  --bucket $GCS_BUCKET \
  --prefix raw/olist

python load_gcs_to_bq.py \
  --project $GCP_PROJECT_ID \
  --dataset $BQ_DATASET_STAGING \
  --bucket $GCS_BUCKET \
  --prefix raw/olist
```

### 4) Build transformations with dbt

```bash
cd ../dbt
pip install dbt-bigquery
cp profiles.yml.example ~/.dbt/profiles.yml
dbt deps
dbt run
dbt test
```

### 5) Start dashboard

From the project root, load env vars first (so `GCP_PROJECT_ID`, `BQ_DATASET_MART`, and credentials apply):

```bash
cd ..
set -a && source .env && set +a
cd dashboard
pip install -r requirements.txt
streamlit run app.py
```

## Dashboard tiles

1. Categorical distribution: revenue by product category
2. Temporal trend: daily lifecycle conversion (`placed -> approved -> delivered`)

## Reproducibility notes

- All transformations are materialized in BigQuery marts
- Data quality checks are implemented in dbt tests
- Partitioning and clustering are applied on mart tables for dashboard workloads
