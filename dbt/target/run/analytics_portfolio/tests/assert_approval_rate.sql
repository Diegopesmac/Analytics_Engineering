
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  -- Fails if any month has approval rate outside [0,1]
with approvals as (
  select
    date_trunc('month', application_date) as month,
    sum(case when approved=1 then 1 else 0 end) as approved_count,
    count(*) as total_count
  from "warehouse"."raw"."proposals"
  group by 1
)

select * from approvals
where (approved_count * 1.0 / nullif(total_count,0)) < 0 or (approved_count * 1.0 / nullif(total_count,0)) > 1
  
  
      
    ) dbt_internal_test