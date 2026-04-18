# Runbook — Como executar localmente

1. Preparar ambiente Python e instalar dependências:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2. Gerar dados e carregar DuckDB:

```powershell
python data/generate_data.py
python scripts/load_to_duckdb.py
```

3. Rodar dbt localmente:

```powershell
cd dbt
copy profiles.yml.template profiles.yml
dbt run --profiles-dir .
dbt test --profiles-dir .
```

4. Subir serviços para orquestração e dashboard (opcional):

```powershell
docker compose up -d --build
```
