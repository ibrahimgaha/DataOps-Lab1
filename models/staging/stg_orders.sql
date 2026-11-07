-- Give each column its type and normalize country names. Keep every row.
select
    try_cast(src.order_id as integer) as order_id,
    try_strptime(src.order_date, '%Y-%m-%d')::date as order_date,
    nullif(trim(src.customer_id), '') as customer_id,
    upper(left(trim(src.country), 1)) || lower(substr(trim(src.country), 2)) as country,
    src.product,
    try_cast(src.quantity as integer) as quantity,
    try_cast(src.unit_price as decimal(10, 2)) as unit_price,
    src._row_number,
    src._source_file,
    src._loaded_at
from {{ source('raw', 'orders') }} as src
