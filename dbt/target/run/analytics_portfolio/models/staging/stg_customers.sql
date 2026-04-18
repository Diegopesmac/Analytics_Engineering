
  
  create view "warehouse"."marts"."stg_customers__dbt_tmp" as (
    

with raw_customers as (
  select * from raw.customers
)

select
  customer_id,
  age,
  income,
  segment
from raw_customers
  );
