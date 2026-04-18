{{
  config(materialized='table')
}}

select
  customer_id,
  min(age) as age,
  avg(income) as income,
  max(segment) as segment
from {{ ref('stg_customers') }}
group by customer_id
