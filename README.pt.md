# Analytics Engineering — Credit Portfolio (Português)

Projeto de portfólio demonstrando um fluxo end-to-end de Analytics Engineering
aplicado a uma carteira de crédito (geração de dados, ingestão raw, transformação
com dbt, qualidade de dados com Great Expectations, orquestração com Airflow e
visualização com Metabase).

Principais componentes
- Origem sintética: `data/generate_data.py`
- Armazenamento analítico: DuckDB (`data/warehouse.duckdb`)
- Transformações: `dbt/` (dbt-core + dbt-duckdb)
- Data quality: `great_expectations/`
- Orquestração: `airflow/dags/credit_pipeline.py` (esqueleto)
- Dashboard: Metabase (exposto via Docker Compose)

Quickstart (local, mínimo)

1) Criar ambiente virtual e instalar dependências

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2) Gerar dados sintéticos (CSV) em `raw_input/`

```powershell
python data/generate_data.py
```

3) Carregar CSVs para DuckDB

```powershell
python scripts/load_to_duckdb.py
```

4) (opcional) Executar pipeline completo via helper

```powershell
python scripts/run_pipeline.py
```

5) (opcional) Rodar dbt manualmente

```powershell
cd dbt
# copie profiles.yml.template -> profiles.yml e ajuste o caminho para ../data/warehouse.duckdb
dbt deps
dbt run --profiles-dir .
dbt test --profiles-dir .
dbt docs generate --profiles-dir .
```

Docker (serviços de apoio)

- Há um `docker-compose.yml` no repositório (Metabase, Airflow, runner). Para subir:

```powershell
docker compose up -d --build
```

Qualidade de dados

- Expectativas ficam em `great_expectations/expectations` e validações em
  `great_expectations/validations`.
- O runner `scripts/run_ge_checks.py` escreve relatórios JSON e falha com
  código de saída não-zero caso expectativas críticas falhem.

Estrutura do projeto (resumo)

- data/: gerador e artefatos de dados (CSV)
- raw_input/: arquivos CSV gerados
- scripts/: utilitários (load_to_duckdb, runners, GE helpers)
- dbt/: projeto dbt (models, profiles.yml.template)
- great_expectations/: expectativas e checkpoints
- airflow/: DAGs de orquestração
- dashboards/: queries e exportações (Metabase)

Execução rápida (exemplo)

```powershell
.\.venv\Scripts\activate
python data/generate_data.py
python scripts/load_to_duckdb.py
python scripts/run_ge_checks.py
cd dbt
dbt run --profiles-dir .
dbt test --profiles-dir .
```

CI / GitHub Actions

- Existe um fluxo básico em `.github/workflows/ci.yml` que gera dados,
  carrega DuckDB e executa comandos dbt em runner CI.

Dicas e troubleshooting

- Se `dbt` não estiver no PATH no Windows, instale com `pip install --user dbt-core dbt-duckdb`
  e ajuste `profiles.yml` conforme `dbt/profiles.yml.template`.
- O loader usa `read_csv_auto` do DuckDB para suportar variações de schema.

Próximos passos sugeridos

- Ajustar e versionar expectativas do Great Expectations (checkpoints)
- Adicionar dashboards exportados do Metabase em `dashboards/`
- Integrar execução no Airflow/Docker runner para CI/CD

Contribuições

Pull requests são bem-vindos. Para mudanças grandes, abra uma issue primeiro
 descrevendo a proposta.

Licença

Código fornecido sem licença explícita — use apenas para aprendizado e portfólio.
