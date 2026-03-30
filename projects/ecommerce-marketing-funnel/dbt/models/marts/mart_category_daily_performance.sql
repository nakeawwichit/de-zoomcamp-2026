{{
    config(
        materialized='table',
        partition_by={"field": "order_date", "data_type": "date"},
        cluster_by=["product_category"]
    )
}}

with orders as (
    select * from {{ ref('stg_olist_orders') }}
),
order_items as (
    select * from {{ ref('stg_olist_order_items') }}
),
products as (
    select * from {{ ref('stg_olist_products') }}
),
translations as (
    select * from {{ ref('stg_category_translation') }}
),
joined as (
    select
        o.order_date,
        coalesce(t.product_category_name_english, p.product_category_name, 'unknown') as product_category,
        oi.order_id,
        oi.price
    from order_items oi
    inner join orders o using (order_id)
    left join products p using (product_id)
    left join translations t using (product_category_name)
)
select
    order_date,
    product_category,
    count(distinct order_id) as orders_count,
    sum(price) as revenue
from joined
group by 1, 2
