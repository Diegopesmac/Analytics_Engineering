# Modelagem de Dados

Camadas:
- `raw` — cópia fiel dos CSVs gerados (sem transformação)
- `staging` — padronização de tipos, limpeza e casting (prefixo `stg_`)
- `marts` — modelos finais orientados a perguntas de negócio (fatos e dimensões)

Principais entidades/modelos:
- `dim_customer` — dimensão de clientes
- `dim_product` — dimensão de produto
- `dim_date` — dimensão de tempo
- `fact_contracts` — parcelas/contratos
- `fact_payments` — pagamentos de parcelas
- `mrt_kpis_carteira` — agregados para dashboard

Regras de negócio exemplares:
- Taxa de aprovação: proporção de `proposals.approved = 1` por período
- Inadimplência: clientes com `missed` em pagamentos em janelas de 30/60 dias
- Ticket médio: `approved_amount` médio por produto
