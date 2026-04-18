"""Run full local pipeline: generate data, load to DuckDB, run GE checks, run dbt run/test/docs.
Designed for local development without Docker.
"""
import subprocess
import sys
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(ROOT, '..'))


def run(cmd, cwd=None):
    print('RUN:', cmd)
    res = subprocess.run(cmd, shell=True, cwd=cwd or PROJECT_ROOT)
    if res.returncode != 0:
        print(f'Command failed: {cmd} (code {res.returncode})')
        sys.exit(res.returncode)


def main():
    # 1. Generate data
    run('python data/generate_data.py')

    # 2. Load to DuckDB
    run('python scripts/load_to_duckdb.py')

    # 3. Create GE suites (optional)
    run('python scripts/create_ge_suites.py')

    # 4. Run GE checks
    run('python scripts/run_ge_checks.py')

    # 5. Run dbt (requires dbt installed and profiles configured)
    dbt_dir = os.path.join(PROJECT_ROOT, 'dbt')
    print('Running dbt in', dbt_dir)

    # Locate dbt executable in typical user script locations on Windows
    def find_dbt_exe():
        appdata = os.environ.get('APPDATA')
        candidates = []
        if appdata:
            candidates.append(os.path.join(appdata, 'Python', 'Python311', 'Scripts', 'dbt.exe'))
        candidates.append(os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Python', 'Python311', 'Scripts', 'dbt.exe'))
        for p in candidates:
            if os.path.exists(p):
                return p
        # fallback to relying on PATH
        return 'dbt'

    dbt_exe = find_dbt_exe()
    print('Using dbt executable:', dbt_exe)

    # run deps (ignore failure), run, test, docs
    try:
        subprocess.run([dbt_exe, 'deps'], cwd=dbt_dir)
    except Exception:
        print('`dbt deps` failed or not found; continuing')
    run(f'"{dbt_exe}" run --profiles-dir .', cwd=dbt_dir)
    run(f'"{dbt_exe}" test --profiles-dir .', cwd=dbt_dir)
    run(f'"{dbt_exe}" docs generate --profiles-dir .', cwd=dbt_dir)

    print('\nPipeline complete. Check great_expectations/validations and dbt/target for outputs.')


if __name__ == '__main__':
    main()
