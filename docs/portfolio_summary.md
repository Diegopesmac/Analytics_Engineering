# Portfolio: Analytics Engineering — Credit Risk

## 1. Resumo executivo
- Objetivo: projeto end-to-end para demonstrar engenharia analítica aplicada a risco de crédito (propostas, contratos, pagamentos, inadimplência).
- Stack: Python, DuckDB, dbt (dbt-duckdb), Great Expectations, Airflow, Metabase. Justificativas e trade-offs documentados em `docs/`.

## 2. Arquitetura proposta
- Fluxo: data generation (CSV) → raw (DuckDB) → staging (dbt) → marts (dbt) → BI (Metabase).
- Orquestração: Airflow DAG `airflow/dags/credit_pipeline.py`.

## 3. Estrutura do repositório
- `data/`: artefato DuckDB (não comitado)
- `raw_input/`: CSVs gerados
- `dbt/`: projeto dbt (models, profiles template, docs)
- `airflow/`: DAGs
- `scripts/`: geração, carga, GE runners, pipeline runner
- `great_expectations/`: expectations, validations, checkpoints
- `dashboards/`: SQLs e export JSON

## 4. Modelagem de dados
- Entidades: customers, proposals, contracts, payments, transactions, products, dim_date.
- Camadas: `raw` (originais), `staging` (`stg_*`), `marts` (fatos/dimensões e `mrt_kpis_carteira`).

## 5. Estratégia de qualidade de dados
- Implementada com Great Expectations (suites JSON em `great_expectations/expectations/`), runner em `scripts/run_ge_checks.py` e outputs em `great_expectations/validations/`.
- GE falha o pipeline (exit code != 0) quando expectativas não se cumprem.

## 6. Estratégia de orquestração
- DAG `credit_pipeline` executa: gerar → carregar → GE checks → `dbt run` → `dbt docs generate`.
- Retries configurados (1 retry, 5min). Logs visíveis na UI do Airflow.

## 7. Dashboard e consumo analítico
- KPIs: approval rate, delinquency rate (30/60-day windows), ticket médio por produto, evolução da carteira.
- Queries em `dashboards/kpis.sql`. Metabase export placeholder em `dashboards/metabase_dashboard.json`.

## 8. Setup e execução
- Quick local (without Docker): see `scripts/run_pipeline.py` (gerar → carregar → GE → dbt run/test/docs).
- Docker Compose to run Airflow and Metabase: `docker compose up -d --build`.

## 9. Evidências e validações
- Exemplos de outputs de validação: `great_expectations/validations/*.json`.
- `dbt/target/` será gerado pelo `dbt docs` (linage/docs).

## 10. Trade-offs e melhorias futuras
- Trade-offs: escolha DuckDB prioriza reprodutibilidade local; para integração empresarial adicionar Postgres auxiliar.
- Melhorias: CI com sqlfluff, testes de integração Airflow, exports automáticos para Metabase via API, visualizações mais ricas.

---

Veja `README.md` e `docs/*.md` para instruções detalhadas.
