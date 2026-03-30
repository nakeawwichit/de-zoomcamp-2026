with source as (
    select * from {{ source('staging', 'stg_olist_products_raw') }}
),
renamed as (
    select
        product_id,
        product_category_name
    from source
)
select * from renamed
