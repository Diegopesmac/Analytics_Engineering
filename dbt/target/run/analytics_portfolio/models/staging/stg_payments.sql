
  
  create view "warehouse"."marts"."stg_payments__dbt_tmp" as (
    

with raw_payments as (
  select * from raw.payments
)

select
  payment_id,
  contract_id,
  installment_number,
  case
    when payment_date is null then null
    when typeof(payment_date) = 'DATE' then payment_date
    when trim(cast(payment_date as varchar)) = '' then null
    else cast(trim(cast(payment_date as varchar)) as date)
  end as payment_date,
  paid_amount,
  status
from raw_payments
  );
