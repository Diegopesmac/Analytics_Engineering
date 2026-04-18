{{
  config(materialized='table')
}}

select
  p.payment_id,
  p.contract_id,
  p.installment_number,
  p.payment_date,
  p.paid_amount,
  p.status
from {{ ref('stg_payments') }} p
