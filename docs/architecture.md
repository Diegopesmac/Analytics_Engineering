# Arquitetura

Visão geral: pipeline analítico em camadas (raw -> staging -> marts) usando DuckDB como armazém local, dbt para transformações, Great Expectations para qualidade e Airflow para orquestração. Metabase é usado para dashboard.

Fluxo ponta a ponta:
- `data/generate_data.py` gera CSVs em `raw_input/` (dados sintéticos)
- `scripts/load_to_duckdb.py` carrega CSVs para `data/warehouse.duckdb` (schema `raw`)
- `dbt` models leem `raw.*` e geram `stg_*` e `marts` (fatos/dimensões)
- Great Expectations executa validações contra tabelas `raw` e `marts`
- Airflow orquestra a sequência (geração -> carga -> checks -> dbt)
- Metabase consulta `marts` para dashboards
