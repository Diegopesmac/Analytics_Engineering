
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    proposal_id as unique_field,
    count(*) as n_records

from "warehouse"."marts"."stg_proposals"
where proposal_id is not null
group by proposal_id
having count(*) > 1



  
  
      
    ) dbt_internal_test