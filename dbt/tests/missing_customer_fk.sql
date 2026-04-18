-- Finds proposals referencing missing customers
select p.*
from {{ source('raw','proposals') }} p
left join {{ source('raw','customers') }} c on p.customer_id = c.customer_id
where c.customer_id is null
