

select
  p.payment_id,
  p.contract_id,
  p.installment_number,
  p.payment_date,
  p.paid_amount,
  p.status
from "warehouse"."marts"."stg_payments" p