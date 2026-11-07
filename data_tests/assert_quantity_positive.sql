select
    order_id,
    quantity
from {{ ref('orders_clean') }}
where quantity is null or quantity <= 0
