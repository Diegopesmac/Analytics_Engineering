

with totals as (
  select
    c.customer_id,
    count(distinct c.contract_id) as n_contracts,
    sum(c.amount_due) as total_due
  from "warehouse"."marts"."fact_contracts" c
  group by c.customer_id
),
payments as (
  select
    f.contract_id,
    sum(f.paid_amount) as total_paid
  from "warehouse"."marts"."fact_payments" f
  group by f.contract_id
)
  ,
  payments_customer as (
  select
    fc.customer_id,
    sum(pay.total_paid) as total_paid
  from payments pay
  join "warehouse"."marts"."fact_contracts" fc
    on pay.contract_id = fc.contract_id
  group by fc.customer_id
)

select
  t.customer_id,
  t.n_contracts,
  t.total_due,
  coalesce(pc.total_paid, 0) as total_paid
from totals t
left join payments_customer pc
  on pc.customer_id = t.customer_id