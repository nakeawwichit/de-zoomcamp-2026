{{
    config(
        materialized='table',
        partition_by={"field": "order_date", "data_type": "date"},
        cluster_by=["order_status"]
    )
}}

with orders as (
    select * from {{ ref('stg_olist_orders') }}
)
select
    order_date,
    order_status,
    count(distinct order_id) as orders_count,
    countif(order_purchase_timestamp is not null) as placed_orders,
    countif(order_approved_at is not null) as approved_orders,
    countif(order_delivered_customer_date is not null) as delivered_orders,
    safe_divide(
        countif(order_approved_at is not null),
        nullif(countif(order_purchase_timestamp is not null), 0)
    ) as placed_to_approved_rate,
    safe_divide(
        countif(order_delivered_customer_date is not null),
        nullif(countif(order_approved_at is not null), 0)
    ) as approved_to_delivered_rate
from orders
group by 1, 2
