"""Create minimal Great Expectations expectation suite files for raw tables.
This script writes simple JSON expectation definitions that can be used by
`scripts/run_ge_checks.py` or manually inspected.
"""
import os
import json

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(ROOT, '..', 'great_expectations', 'expectations')
os.makedirs(OUT_DIR, exist_ok=True)

SPECS = {
    'customers': [
        {'expectation_type': 'expect_column_to_exist', 'kwargs': {'column': 'customer_id'}},
        {'expectation_type': 'expect_column_values_to_not_be_null', 'kwargs': {'column': 'customer_id'}},
    ],
    'proposals': [
        {'expectation_type': 'expect_column_to_exist', 'kwargs': {'column': 'proposal_id'}},
        {'expectation_type': 'expect_column_values_to_be_in_set', 'kwargs': {'column': 'approved', 'value_set': [0,1]}},
    ],
    'contracts': [
        {'expectation_type': 'expect_column_to_exist', 'kwargs': {'column': 'contract_id'}},
    ],
    'payments': [
        {'expectation_type': 'expect_column_to_exist', 'kwargs': {'column': 'payment_id'}},
    ],
    'transactions': [
        {'expectation_type': 'expect_column_to_exist', 'kwargs': {'column': 'transaction_id'}},
    ],
}


def main():
    for table, exps in SPECS.items():
        out = {
            'expectation_suite_name': f'raw.{table}.suite',
            'expectations': []
        }
        for e in exps:
            out['expectations'].append({'expectation_type': e['expectation_type'], 'kwargs': e['kwargs']})
        path = os.path.join(OUT_DIR, f'{table}.json')
        with open(path, 'w', encoding='utf8') as f:
            json.dump(out, f, indent=2)
        print('Wrote', path)


if __name__ == '__main__':
    main()
