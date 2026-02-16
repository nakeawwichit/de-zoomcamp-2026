SELECT 
    dispatching_base_num, 
    count(*) as cnt
FROM `<project_id>.trips_data_all.fhv_tripdata`
GROUP BY 1
ORDER BY cnt DESC
LIMIT 10;