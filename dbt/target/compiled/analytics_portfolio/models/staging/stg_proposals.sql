

with raw_proposals as (
  select * from raw.proposals
)

select
  proposal_id,
  customer_id,
  product_id,
  cast(application_date as date) as application_date,
  approved,
  approved_amount
from raw_proposals