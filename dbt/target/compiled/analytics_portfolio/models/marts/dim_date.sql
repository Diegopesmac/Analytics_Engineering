

with dates as (
  select distinct date(due_date) as d from raw.contracts
  union
  select distinct date(application_date) as d from raw.proposals
  union
  select distinct date(transaction_date) as d from raw.transactions
)

select
  d as date,
  extract(year from d) as year,
  extract(month from d) as month,
  extract(day from d) as day
from dates