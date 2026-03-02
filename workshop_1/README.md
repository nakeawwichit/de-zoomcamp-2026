# Workshop 1: Ingestion with dlt

NYC Taxi trip data pipeline using [dlt](https://dlthub.com/docs) → DuckDB

## Pipeline

ดึงข้อมูลจาก paginated REST API แล้วโหลดลง DuckDB

```
API (10 pages × 1,000 records) → dlt → DuckDB
```

### Run

```bash
cd my-dlt-pipeline
source .venv/bin/activate
python taxi_pipeline.py
```

## Homework Answers

| #   | Question               | Answer                       |
| --- | ---------------------- | ---------------------------- |
| 1   | Start/End date         | **2009-06-01 to 2009-07-01** |
| 2   | Credit card proportion | **26.66%** (2,666 / 10,000)  |
| 3   | Total tips             | **$6,063.41**                |

## Tech Stack

- **dlt** — data load tool
- **DuckDB** — local data warehouse
- **Python 3.13** — runtime
