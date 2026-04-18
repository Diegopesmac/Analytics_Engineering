DBT project: analytics_portfolio

Quick steps to run locally:

1. Ensure `dbt-core` and `dbt-duckdb` are installed in your Python environment.
2. From `dbt/` copy `profiles.yml.template` to `profiles.yml` (or set `DBT_PROFILES_DIR` env).
3. Run: `dbt deps || true && dbt run --profiles-dir . && dbt test --profiles-dir . && dbt docs generate --profiles-dir .`

Notes:
- The project expects DuckDB file at `../data/warehouse.duckdb` and `raw.*` tables created by `scripts/load_to_duckdb.py`.
- Models are organized under `models/staging` and `models/marts`.
