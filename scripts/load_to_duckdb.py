"""Load CSV files from raw_input/ into a DuckDB file at data/warehouse.duckdb
Creates schema `raw` and tables named after CSV files (without extension).
"""
import os
import duckdb

ROOT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(ROOT, '..', 'raw_input')
DB_PATH = os.path.join(ROOT, '..', 'data', 'warehouse.duckdb')
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def load_all():
    con = duckdb.connect(DB_PATH)
    for fname in os.listdir(RAW):
        if not fname.lower().endswith('.csv'):
            continue
        table = os.path.splitext(fname)[0]
        path = os.path.join(RAW, fname)
        print(f'Loading {path} -> {table} (schema raw)')
        con.execute("CREATE SCHEMA IF NOT EXISTS raw")
        # Create or replace table from CSV using read_csv_auto
        try:
            con.execute(f"DROP TABLE IF EXISTS raw.{table}")
        except Exception:
            pass
        con.execute(f"CREATE TABLE raw.{table} AS SELECT * FROM read_csv_auto('{path}', header=True)")
    con.close()
    print('Load complete. DuckDB file at', DB_PATH)


if __name__ == '__main__':
    load_all()
