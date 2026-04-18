from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'analytics_portfolio',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='credit_pipeline',
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval='@daily',
    catchup=False,
) as dag:

    generate = BashOperator(
        task_id='generate_data',
        bash_command='python /workspace/data/generate_data.py'
    )

    load = BashOperator(
        task_id='load_to_duckdb',
        bash_command='python /workspace/scripts/load_to_duckdb.py'
    )

    ge_checks = BashOperator(
        task_id='run_ge_checks',
        bash_command='python /workspace/scripts/run_ge_checks.py'
    )

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /workspace/dbt && dbt run --profiles-dir /workspace/dbt'
    )

    dbt_docs = BashOperator(
        task_id='dbt_docs_generate',
        bash_command='cd /workspace/dbt && dbt docs generate --profiles-dir /workspace/dbt'
    )

    generate >> load >> ge_checks >> dbt_run >> dbt_docs
