
  
    
    

    create  table
      "warehouse"."marts"."dim_product__dbt_tmp"
  
    as (
      

select
  product_id,
  product_name,
  term_months
from raw.products
    );
  
  