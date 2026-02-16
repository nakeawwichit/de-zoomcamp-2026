-- สร้าง External Table สำหรับ Yellow Taxi (รวมทุกปี/เดือนที่อยู่ใน GCS)
CREATE OR REPLACE EXTERNAL TABLE `<project_id>.trips_data_all.yellow_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://taxi-data-jan-june-2024/yellow/yellow_tripdata_*.parquet']
);

-- สร้าง External Table สำหรับ Green Taxi
CREATE OR REPLACE EXTERNAL TABLE `<project_id>.trips_data_all.green_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://taxi-data-jan-june-2024/green/green_tripdata_*.parquet']
);

-- สร้าง External Table สำหรับ FHV (สำคัญมากสำหรับการบ้านข้อหลังๆ)
CREATE OR REPLACE EXTERNAL TABLE `<project_id>.trips_data_all.fhv_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://taxi-data-jan-june-2024/fhv/fhv_tripdata_*.parquet']
);