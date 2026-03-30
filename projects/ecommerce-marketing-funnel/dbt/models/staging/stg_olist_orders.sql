with source as (
    select * from {{ source('staging', 'stg_olist_orders_raw') }}
),
renamed as (
    select
        order_id,
        customer_id,
        order_status,
        timestamp(order_purchase_timestamp) as order_purchase_timestamp,
        timestamp(order_approved_at) as order_approved_at,
        timestamp(order_delivered_customer_date) as order_delivered_customer_date,
        date(order_purchase_timestamp) as order_date
    from source
)
select * from renamed
