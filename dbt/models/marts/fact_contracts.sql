{{
  config(materialized='table')
}}

select
  c.contract_id,
  c.proposal_id,
  c.customer_id,
  c.installment_number,
  c.due_date,
  c.amount_due
from {{ ref('stg_contracts') }} c
