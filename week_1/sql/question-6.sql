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