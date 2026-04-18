
    
    

select
    contract_id as unique_field,
    count(*) as n_records

from "warehouse"."marts"."stg_contracts"
where contract_id is not null
group by contract_id
having count(*) > 1


