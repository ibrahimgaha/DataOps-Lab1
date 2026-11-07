-- A failed batch stops before dbt builds the reporting tables.
select
    count(*) filter (where reject_reason is not null) as n_rejected,
    count(*) as n_total
from {{ ref('int_orders_checked') }}
having
    count(*) = 0
    or count(*) filter (where reject_reason is not null) > 0.20 * count(*)
