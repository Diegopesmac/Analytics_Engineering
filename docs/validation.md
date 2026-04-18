# Validação de Dados (Great Expectations)

O projeto inclui validações básicas de qualidade de dados usando Great Expectations. Implementações e scripts:

- `scripts/create_ge_suites.py`: gera JSONs mínimos de expectativas para cada tabela `raw`.
- `scripts/run_ge_checks.py`: executa expectativas (via `PandasDataset`) e grava resultados em `great_expectations/validations/*.json`.
- `great_expectations/checkpoints/checkpoint_all.yml`: placeholder de checkpoint que pode ser integrado com um `DataContext` completo.

Comportamento de falha:
- `scripts/run_ge_checks.py` retorna código de saída `1` se qualquer expectativa falhar, e `2` em caso de erro inesperado. O DAG Airflow e o CI usam esse código para marcar falhas no pipeline.

Execução local rápida:

```powershell
python scripts/create_ge_suites.py
python scripts/run_ge_checks.py
```

Resultados são salvos em `great_expectations/validations/` como JSON legíveis.
