import duckdb
import os
import requests

# 1. Download Taxi Zone Lookup (if missing)
ZONE_FILE = "taxi_zone_lookup.csv"
if not os.path.exists(ZONE_FILE):
    url = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"
    print(f"Downloading {url}...")
    try:
        r = requests.get(url)
        r.raise_for_status()
        with open(ZONE_FILE, "wb") as f:
            f.write(r.content)
        print("Download complete.")
    except Exception as e:
        print(f"Failed to download zone file: {e}")

# 2. Setup DuckDB
con = duckdb.connect()

# 3. Create Views
# Note: Using union_by_name=True to safely handle schema evolution (e.g., int/double mismatch)
print("\nCreating Views...")
try:
    con.execute("CREATE OR REPLACE VIEW yellow_tripdata AS SELECT * FROM read_parquet('downloads/yellow/*.parquet', union_by_name=True);")
    con.execute("CREATE OR REPLACE VIEW green_tripdata AS SELECT * FROM read_parquet('downloads/green/*.parquet', union_by_name=True);")
    con.execute("CREATE OR REPLACE VIEW fhv_tripdata AS SELECT * FROM read_parquet('downloads/fhv/*.parquet', union_by_name=True);")
    con.execute(f"CREATE OR REPLACE VIEW zones AS SELECT * FROM read_csv_auto('{ZONE_FILE}');")
    print("Views created successfully.")
except Exception as e:
    print(f"Error creating views: {e}")

# 4. Queries

# Q3: Monthly Records (Yellow + Green, Aggregated per Zone)
# Note: Simulating fct_monthly_zone_revenue
print("\n--- Query 1: Monthly Records (Yellow + Green, Aggregated) ---")
q1 = """
SELECT count(*) as total_rows
FROM (
    SELECT 
        date_trunc('month', tpep_pickup_datetime) as pickup_month, 
        PULocationID 
    FROM yellow_tripdata
    GROUP BY 1, 2

    UNION ALL

    SELECT 
        date_trunc('month', lpep_pickup_datetime) as pickup_month, 
        PULocationID 
    FROM green_tripdata
    GROUP BY 1, 2
);
"""
try:
    con.sql(q1).show()
except Exception as e:
    print(f"Error in Q1: {e}")


# Q4: Highest Revenue Zone (Green Taxi 2020)
print("\n--- Query 2: Highest Revenue Zone (Green 2020) ---")
q2 = """
SELECT 
    z.Zone,
    SUM(total_amount) as revenue
FROM green_tripdata g
JOIN zones z ON g.PULocationID = z.LocationID
WHERE year(lpep_pickup_datetime) = 2020
GROUP BY 1
ORDER BY 2 DESC
LIMIT 1;
"""
try:
    con.sql(q2).show()
except Exception as e:
    print(f"Error in Q2: {e}")


# Q5: Green Trips Oct 2019
print("\n--- Query 3: Green Trips Oct 2019 ---")
q3 = """
SELECT count(*) as count
FROM green_tripdata
WHERE lpep_pickup_datetime >= '2019-10-01' 
  AND lpep_pickup_datetime < '2019-11-01';
"""
try:
    con.sql(q3).show()
except Exception as e:
    print(f"Error in Q3: {e}")


# Q6: FHV Null Dispatching Bases (2019)
print("\n--- Query 4: FHV Null Dispatching Bases (2019) ---")
q4 = """
SELECT count(*) as count
FROM fhv_tripdata
WHERE year(pickup_datetime) = 2019
  AND dispatching_base_num IS NULL;
"""
try:
    con.sql(q4).show()
except Exception as e:
    print(f"Error in Q4: {e}")
