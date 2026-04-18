 # Analytics Engineering — Credit Portfolio (English)

 A portfolio project demonstrating an end-to-end Analytics Engineering workflow
for a credit portfolio: synthetic data generation, raw ingestion, transformations
with dbt, data quality checks with Great Expectations, orchestration with
Airflow, and a dashboard via Metabase.

Key components
- Synthetic data generator: `data/generate_data.py`
- Analytical store: DuckDB (`data/warehouse.duckdb`)
- Transformations: `dbt/` (dbt-core + dbt-duckdb)
- Data quality: `great_expectations/`
- Orchestration: `airflow/dags/credit_pipeline.py` (skeleton)
- Dashboard: Metabase (via Docker Compose)

Quickstart (local, minimal)

1) Create a Python virtual environment and install dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2) Generate synthetic CSVs into `raw_input/`

```powershell
python data/generate_data.py
```

3) Load CSVs into DuckDB

```powershell
python scripts/load_to_duckdb.py
```

4) (optional) Run the full pipeline helper

```powershell
python scripts/run_pipeline.py
```

5) (optional) Run dbt manually

```powershell
cd dbt
# copy profiles.yml.template -> profiles.yml and point to ../data/warehouse.duckdb
dbt deps
dbt run --profiles-dir .
dbt test --profiles-dir .
dbt docs generate --profiles-dir .
```

Docker (support services)

- There is a `docker-compose.yml` (Metabase, Airflow, runner). To bring up:

```powershell
docker compose up -d --build
```

Data quality

- Expectations are stored in `great_expectations/expectations` and validations
	in `great_expectations/validations`.
- The runner `scripts/run_ge_checks.py` writes validation JSONs and exits with
	a non-zero code when critical expectations fail.

Project layout (summary)

- data/: generator and data artifacts (CSV)
- raw_input/: generated CSVs
- scripts/: utilities (load_to_duckdb, runners, GE helpers)
- dbt/: dbt project (models, profiles.yml.template)
- great_expectations/: expectations and checkpoints
- airflow/: orchestration DAGs
- dashboards/: queries and Metabase exports

Quick run example

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

- A basic CI workflow exists in `.github/workflows/ci.yml` that generates data,
	loads DuckDB and runs dbt commands on the CI runner.

Tips & troubleshooting

- If `dbt` is not on your Windows PATH, install with `pip install --user dbt-core dbt-duckdb`
	and copy/adjust `dbt/profiles.yml.template`.
- The loader uses DuckDB's `read_csv_auto` to tolerate schema variations.

Suggested next steps

- Harden and version Great Expectations checkpoints
- Add exported Metabase dashboards into `dashboards/`
- Integrate full execution into Airflow/Docker runner for CI/CD

Contributing

Pull requests welcome. For large changes, open an issue describing your plan first.

License

No explicit license provided — use for learning and portfolio purposes only.
