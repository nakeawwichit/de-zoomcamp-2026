SELECT COUNT(*) AS count_up_to_1_mile
FROM green_tripdata
WHERE trip_distance <= 1
  AND lpep_pickup_datetime >= '2025-11-01'
  AND lpep_pickup_datetime  < '2025-12-01';