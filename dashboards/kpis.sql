-- KPIs SQL for Metabase / ad-hoc queries against marts

-- Approval rate by month
select
  date_trunc('month', application_date) as month,
  count(*) filter (where approved = 1) as approved_count,
  count(*) as total_apps,
  1.0 * count(*) filter (where approved = 1) / nullif(count(*),0) as approval_rate
from raw.proposals
group by 1
order by 1 desc;

-- Delinquency rate (clients with any missed payment in last 90 days)
select
  count(distinct p.customer_id) filter (where exists (select 1 from raw.payments rp where rp.contract_id = c.contract_id and rp.status = 'missed' and cast(rp.payment_date as date) >= current_date - 90)) as delinquent_customers,
  count(distinct c.customer_id) as total_customers,
  1.0 * count(distinct p.customer_id) filter (where exists (select 1 from raw.payments rp where rp.contract_id = c.contract_id and rp.status = 'missed' and cast(rp.payment_date as date) >= current_date - 90)) / nullif(count(distinct c.customer_id),0) as delinquency_rate
from raw.contracts c
left join raw.proposals p on p.proposal_id = c.proposal_id;

-- Ticket médio de contratos aprovados por produto
select
  p.product_id,
  avg(p.approved_amount) as avg_ticket
from raw.proposals p
where p.approved = 1
group by 1
order by 2 desc;
