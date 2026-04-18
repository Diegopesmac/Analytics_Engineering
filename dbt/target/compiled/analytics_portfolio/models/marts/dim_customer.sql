

select
  customer_id,
  min(age) as age,
  avg(income) as income,
  max(segment) as segment
from "warehouse"."marts"."stg_customers"
group by customer_id