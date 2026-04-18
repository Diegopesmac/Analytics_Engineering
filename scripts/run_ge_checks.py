"""Run basic Great Expectations checks against DuckDB tables and store validation results.
This script uses PandasDataset expectations for simplicity and reproducibility.
"""
import os
import json
import sys
import duckdb
import pandas as pd

# For compatibility across Great Expectations versions, use a lightweight fallback
# if `PandasDataset` is not available. We'll implement minimal expectation checks
# directly using pandas so the runner works in this environment.

ROOT = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT, '..', 'data', 'warehouse.duckdb')
OUT = os.path.join(ROOT, '..', 'great_expectations', 'validations')
os.makedirs(OUT, exist_ok=True)


def validate_table(con, table_name, expectations):
    df = con.execute(f"SELECT * FROM raw.{table_name}").df()
    results = {'table': table_name, 'results': []}
    for exp in expectations:
        ename = exp['name']
        args = exp.get('args', {})
        try:
            if ename == 'expect_column_values_to_not_be_null':
                col = args['column']
                success = df[col].notnull().all()
                details = {'null_count': int(df[col].isnull().sum())}
            elif ename == 'expect_column_values_to_be_between':
                col = args['column']
                minv = args.get('min_value')
                maxv = args.get('max_value')
                series = pd.to_numeric(df[col], errors='coerce')
                success = series.dropna().between(minv, maxv).all()
                details = {'out_of_range_count': int((~series.between(minv, maxv)).sum())}
            elif ename == 'expect_column_values_to_be_in_set' or ename == 'expect_column_values_to_be_in_set':
                col = args['column']
                valset = set(args.get('value_set', []))
                success = df[col].dropna().isin(valset).all()
                details = {'bad_values_count': int((~df[col].isin(valset)).sum())}
            elif ename == 'expect_column_to_exist':
                col = args['column']
                success = col in df.columns
                details = {'exists': success}
            else:
                success = False
                details = {'error': f'Unsupported expectation {ename}'}

            results['results'].append({'expectation': ename, 'success': bool(success), 'details': details})
        except Exception as e:
            results['results'].append({'expectation': ename, 'success': False, 'error': str(e)})
    out_path = os.path.join(OUT, f"{table_name}.json")
    with open(out_path, 'w', encoding='utf8') as f:
        json.dump(results, f, default=str, indent=2)
    print(f'Validation for {table_name} written to {out_path}')


def main():
    con = duckdb.connect(DB_PATH)

    # Define simple expectations per table
    specs = {
        'customers': [
            {'name': 'expect_column_values_to_not_be_null', 'args': {'column': 'customer_id'}},
            {'name': 'expect_column_values_to_be_between', 'args': {'column': 'age', 'min_value': 18, 'max_value': 100}},
        ],
        'proposals': [
            {'name': 'expect_column_values_to_not_be_null', 'args': {'column': 'proposal_id'}},
            {'name': 'expect_column_values_to_be_in_set', 'args': {'column': 'approved', 'value_set': [0,1]}},
        ],
        'contracts': [
            {'name': 'expect_column_values_to_not_be_null', 'args': {'column': 'contract_id'}},
        ],
        'payments': [
            {'name': 'expect_column_values_to_not_be_null', 'args': {'column': 'payment_id'}},
        ],
        'transactions': [
            {'name': 'expect_column_values_to_not_be_null', 'args': {'column': 'transaction_id'}},
        ],
    }

    for table, exps in specs.items():
        try:
            validate_table(con, table, exps)
        except Exception as e:
            print(f'Error validating {table}:', e)
            # treat unexpected errors as failures
            con.close()
            sys.exit(2)

    con.close()
    # Inspect validation outputs and exit non-zero if any expectation failed
    any_failed = False
    val_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'great_expectations', 'validations')
    for fname in os.listdir(val_dir):
        if not fname.endswith('.json'):
            continue
        with open(os.path.join(val_dir, fname), 'r', encoding='utf8') as f:
            data = json.load(f)
            for r in data.get('results', []):
                # GE PandasDataset returns dicts, success may be nested
                if isinstance(r, dict):
                    success = r.get('success')
                    if success is False:
                        any_failed = True
    if any_failed:
        print('One or more GE expectations failed.')
        sys.exit(1)
    else:
        print('All GE expectations passed.')


if __name__ == '__main__':
    main()
