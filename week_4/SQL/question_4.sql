SELECT 
    service_type, 
    count(*) as total_records
FROM `de-zoomcamp-484115.trips_data_all.fact_trips`
-- ปรับเงื่อนไขวันที่ตามที่โจทย์ระบุ (ปกติคือปี 2019-2020)
WHERE pickup_datetime >= '2019-01-01' AND pickup_datetime < '2021-01-01'
GROUP BY 1;