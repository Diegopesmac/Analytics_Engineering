{{
  config(materialized='view')
}}

with raw_tx as (
  select * from raw.transactions
)

select
  transaction_id,
  customer_id,
  cast(transaction_date as date) as transaction_date,
  amount,
  channel
from raw_tx
