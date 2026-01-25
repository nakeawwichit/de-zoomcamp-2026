SELECT z."Zone" AS pickup_zone,
SUM(t.total_amount) AS total_revenue
FROM green_tripdata t
JOIN taxi_zone_lookup z
ON t."PULocationID" = z."LocationID"
WHERE DATE(t.lpep_pickup_datetime) = '2025-11-18'
GROUP BY z."Zone"
ORDER BY total_revenue DESC
LIMIT 1;