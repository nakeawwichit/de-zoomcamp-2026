SELECT DATE(lpep_pickup_datetime) AS pickup_day, trip_distance
FROM green_tripdata
WHERE trip_distance < 100
ORDER BY trip_distance DESC
LIMIT 1;