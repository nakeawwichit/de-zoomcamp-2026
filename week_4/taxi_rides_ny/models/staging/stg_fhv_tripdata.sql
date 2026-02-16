{{ config(materialized='view') }}

with tripdata as 
(
  select *
  from {{ source('raw','fhv_tripdata') }}
  where dispatching_base_num is not null 
)
select
    -- identifiers
    dispatching_base_num,
    cast(pulocationid as integer) as pickup_locationid,
    cast(dolocationid as integer) as dropoff_locationid,
    
    -- timestamps
    cast(pickup_datetime as timestamp) as pickup_datetime,
    cast(dropoff_datetime as timestamp) as dropoff_datetime,
    
    -- trip info
    sr_flag,
    affiliated_base_number
from tripdata

-- กรองข้อมูลปี 2019 ตามที่โจทย์กำหนด
where pickup_datetime >= '2019-01-01' and pickup_datetime < '2020-01-01'