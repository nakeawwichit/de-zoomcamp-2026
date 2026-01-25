### Data Engineering Zoomcamp 2026 - Week 1 Homework

#### Project Structure

- docker/ - docker-compose setup for Postgres
- parquet-to-csv/ - convert parquet files to CSV using Python
- sql/ - SQL queries for each homework question

#### Question 1
```
docker run -it --entrypoint bash python:3.13
pip --version
```
Answer: 25.3

#### Question 2

Answer: db:5433

#### Question 3
```
SELECT COUNT(*) AS count_up_to_1_mile
FROM green_tripdata
WHERE trip_distance <= 1
AND lpep_pickup_datetime >= '2025-11-01'
AND lpep_pickup_datetime < '2025-12-01';
```
Answer: 8,007

#### Question 4
```
SELECT DATE(lpep_pickup_datetime) AS pickup_day, trip_distance
FROM green_tripdata
WHERE trip_distance < 100
ORDER BY trip_distance DESC
LIMIT 1;
```
Answer: 2025-11-14

#### Question 5
```
SELECT z."Zone" AS pickup_zone,
SUM(t.total_amount) AS total_revenue
FROM green_tripdata t
JOIN taxi_zone_lookup z
ON t."PULocationID" = z."LocationID"
WHERE DATE(t.lpep_pickup_datetime) = '2025-11-18'
GROUP BY z."Zone"
ORDER BY total_revenue DESC
LIMIT 1;
```
Answer: East Harlem North

#### Question 6
``` 
SELECT z_do."Zone" AS dropoff_zone,
t.tip_amount
FROM green_tripdata t
JOIN taxi_zone_lookup z_pu
ON t."PULocationID" = z_pu."LocationID"
JOIN taxi_zone_lookup z_do
ON t."DOLocationID" = z_do."LocationID"
WHERE z_pu."Zone" = 'East Harlem North'
AND t.lpep_pickup_datetime >= '2025-11-01'
AND t.lpep_pickup_datetime < '2025-12-01'
ORDER BY t.tip_amount DESC
LIMIT 1;
```
Answer: Yorkville West

#### Question 7

Answer: terraform init, terraform apply --auto-approve, terraform destroy

