with source as (
    select * from {{ source('staging', 'stg_olist_order_items_raw') }}
),
renamed as (
    select
        order_id,
        cast(order_item_id as int64) as order_item_id,
        product_id,
        seller_id,
        cast(price as numeric) as price,
        cast(freight_value as numeric) as freight_value
    from source
)
select * from renamed
