
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  -- Finds proposals referencing missing customers
select p.*
from "warehouse"."raw"."proposals" p
left join "warehouse"."raw"."customers" c on p.customer_id = c.customer_id
where c.customer_id is null
  
  
      
    ) dbt_internal_test