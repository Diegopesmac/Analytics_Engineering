
  
  create view "warehouse"."marts"."stg_contracts__dbt_tmp" as (
    

with raw_contracts as (
  select * from raw.contracts
),

ranked as (
  select
    *,
    case
      when due_date is null then null
      when typeof(due_date) = 'DATE' then due_date
      when trim(cast(due_date as varchar)) = '' then null
      else cast(trim(cast(due_date as varchar)) as date)
    end as due_date_parsed,
    row_number() over (
      partition by contract_id
      order by case
        when due_date is null then date('1970-01-01')
        when typeof(due_date) = 'DATE' then due_date
        else cast(trim(cast(due_date as varchar)) as date)
      end desc
    ) as rn
  from raw_contracts
)

select
  contract_id,
  proposal_id,
  customer_id,
  installment_number,
  due_date_parsed as due_date,
  amount_due
from ranked
where rn = 1
  );
