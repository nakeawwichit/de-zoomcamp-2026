SELECT 
    count(*) 
FROM `<project_id>.trips_data_all.stg_green_tripdata`
WHERE 
    EXTRACT(MONTH FROM pickup_datetime) = 10 
    AND EXTRACT(YEAR FROM pickup_datetime) = 2019;