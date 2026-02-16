# NYC Taxi Analytics Pipeline (Data Engineering Zoomcamp - Module 4)

This project focuses on building an analytics pipeline for NYC Taxi data (Yellow, Green, and FHV) using **dbt** and **BigQuery**. The goal is to transform raw trip data into analytical marts for business intelligence, handling data quality issues and complex aggregations along the way.

## 🚀 Tech Stack

- **Data Warehouse**: Google BigQuery
- **Transformation**: dbt (Data Build Tool)
- **Orchestration/Loading**: Python `web_to_gcs.py` (Custom Script)
- **Local Testing**: DuckDB (for rapid validation)
- **Language**: SQL (Jinja), Python

## 🛠 Project Structure

```bash
week_4/
├── SQL/                   # Ad-hoc SQL queries for initial exploration
├── scripts/               # Python ETL scripts
│   ├── web_to_gcs.py      # Main loader: Download -> Standardize Schema -> GCS -> BigQuery
│   ├── analyze_duckdb.py  # Local analysis script using DuckDB
│   └── service_account.json # (Gitignored) Google Cloud credentials
├── taxi_rides_ny/         # dbt project root
│   ├── models/
│   │   ├── staging/       # Staging models (View) - Cleaning raw data
│   │   │   ├── stg_yellow_tripdata.sql
│   │   │   ├── stg_green_tripdata.sql
│   │   │   └── stg_fhv_tripdata.sql
│   │   ├── core/          # Core models (Table) - Dimensional modeling
│   │   │   ├── dim_zones.sql
│   │   │   ├── fact_trips.sql
│   │   │   └── fct_monthly_zone_revenue.sql
│   └── ...
└── README.md
```

## 💡 Key Technical Challenges & Solutions

### 1. Data Quality Control

**Challenge**: The raw data contained outliers, such as trips with future dates (e.g., year 2090) and invalid records (zero distance/fare).
**Solution**: Implemented robust filters in the dbt staging models.

- **Date Filtering**: Applied strict `WHERE` clauses (e.g., `2019 <= year < 2021`) to filter out bad data at the source.
- **Null Handling**: Filtered out records with missing `VendorID` or `Dispatching_base_num`.

### 2. Schema Evolution Handling (`ehail_fee`)

**Challenge**: The `ehail_fee` column in Green Taxi data changed from `FLOAT` to `INTEGER` across different monthly files, causing BigQuery load failures with standard schema detection.
**Solution**:

- Developed a schema standardization layer in `web_to_gcs.py` using **Pandas**.
- Forced critical columns like `ehail_fee`, `SR_Flag`, and `PUlocationID` to `FLOAT64` before uploading to GCS.
- Configured dbt to cast these fields consistently in staging models to handle mixed types gracefully.

### 3. Complex Aggregations

**Challenge**: Calculating monthly revenue trends across different zones and services required joining multiple large tables.
**Solution**: Created the `fct_monthly_zone_revenue` model that joins trip data with `taxi_zone_lookup`, aggregating metrics like total revenue, trip count, and fare breakdown by Month and Zone. This pre-computed table significantly speeds up dashboard queries.

## 🏃‍♀️ How to Run

### Prerequisites

- Google Cloud Platform Account (BigQuery & GCS enabled).
- Python 3.9+ with `dbt-bigquery`, `pandas`, `google-cloud-storage`, `duckdb` installed.

### Step 1: Load Data to BigQuery

Run the python script to download, process, and load data:

```bash
cd scripts
# Ensure service_account.json is present
python web_to_gcs.py
```

_Note: This script downloads data for Yellow (2019-2020), Green (2019-2020), and FHV (2019)._

### Step 2: Run dbt Transformation

Navigate to the dbt project folder and build the models:

```bash
cd taxi_rides_ny
dbt deps
dbt build --var 'is_test_run: false'
```

### Step 3: Verify Data Quality

Run dbt tests to ensure data integrity (unique keys, not null constraints):

```bash
dbt test
```

## 📚 Lessons Learned

1.  **Schema Enforcement**: While modern data warehouses support schema evolution, consistent data types (like `FLOAT` vs `INT`) are critical for reliability. Handling this upstream (during loading via Python/Pandas) proved much cleaner than trying to fix it in SQL after loading.
2.  **Incremental Staging**: Adding `WHERE` clauses in staging models to filter years (e.g., `2019-2021`) dramatically improves data quality downstream and prevents skew metrics.
3.  **Local Dev with DuckDB**: Using DuckDB for quick sanity checks on Parquet files saved significant time compared to repeatedly uploading to BigQuery for testing every small change.
