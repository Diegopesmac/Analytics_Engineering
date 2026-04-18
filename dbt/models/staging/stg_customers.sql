{{
  config(materialized='view')
}}

with raw_customers as (
  select * from raw.customers
)

select
  customer_id,
  age,
  income,
  segment
from raw_customers
