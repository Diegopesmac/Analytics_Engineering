"""Generate synthetic datasets for credit risk portfolio demo.
Produces CSV files into `raw_input/`.
"""
import os
import random
from datetime import date, timedelta
import pandas as pd


ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, '..', 'raw_input')
os.makedirs(OUT, exist_ok=True)


def mk_customers(n=500):
    rows = []
    for i in range(1, n + 1):
        rows.append({
            'customer_id': f'C{i:05d}',
            'age': random.randint(21, 75),
            'income': round(random.uniform(15000, 250000), 2),
            'segment': random.choice(['retail', 'affluent', 'mass'])
        })
    return pd.DataFrame(rows)


def mk_products():
    return pd.DataFrame([
        {'product_id': 'P01', 'product_name': 'Personal Loan', 'term_months': 24},
        {'product_id': 'P02', 'product_name': 'Credit Card', 'term_months': 12},
        {'product_id': 'P03', 'product_name': 'Auto Loan', 'term_months': 36},
    ])


def mk_proposals(customers, products, n=800):
    rows = []
    for i in range(1, n + 1):
        cust = customers.sample(1).iloc[0]
        prod = products.sample(1).iloc[0]
        app_date = date.today() - timedelta(days=random.randint(0, 720))
        approved = random.random() < 0.7
        amount = round(random.uniform(1000, 50000), 2) if approved else round(random.uniform(1000, 50000), 2)
        rows.append({
            'proposal_id': f'PR{i:06d}',
            'customer_id': cust.customer_id,
            'product_id': prod.product_id,
            'application_date': app_date.isoformat(),
            'approved': int(approved),
            'approved_amount': amount if approved else 0.0
        })
    return pd.DataFrame(rows)


def mk_contracts(proposals):
    rows = []
    contract_id = 1
    for _, p in proposals.iterrows():
        if p.approved:
            start = pd.to_datetime(p.application_date).date() + timedelta(days=7)
            term = random.choice([12, 24, 36])
            monthly = round(p.approved_amount / term, 2)
            for m in range(1, term + 1):
                due = (start + pd.DateOffset(months=m-1)).date()
                rows.append({
                    'contract_id': f'CT{contract_id:07d}',
                    'proposal_id': p.proposal_id,
                    'customer_id': p.customer_id,
                    'installment_number': m,
                    'due_date': due.isoformat(),
                    'amount_due': monthly
                })
            contract_id += 1
    return pd.DataFrame(rows)


def mk_payments(contracts):
    rows = []
    pay_id = 1
    for _, c in contracts.iterrows():
        paid = random.random() < 0.9
        delay_days = random.choice([0, 0, 0, 5, 10, 30, 60]) if not paid else 0
        payment_date = pd.to_datetime(c.due_date).date() + timedelta(days=delay_days) if paid else ''
        paid_amount = c.amount_due if paid else 0.0
        rows.append({
            'payment_id': f'PM{pay_id:08d}',
            'contract_id': c.contract_id,
            'installment_number': c.installment_number,
            'payment_date': payment_date.isoformat() if payment_date else '',
            'paid_amount': paid_amount,
            'status': 'paid' if paid else 'missed'
        })
        pay_id += 1
    return pd.DataFrame(rows)


def mk_transactions(customers, n=2000):
    rows = []
    for i in range(1, n + 1):
        cust = customers.sample(1).iloc[0]
        tdate = date.today() - timedelta(days=random.randint(0, 720))
        rows.append({
            'transaction_id': f'TX{i:07d}',
            'customer_id': cust.customer_id,
            'transaction_date': tdate.isoformat(),
            'amount': round(random.uniform(5, 2000), 2),
            'channel': random.choice(['online', 'branch', 'pos'])
        })
    return pd.DataFrame(rows)


def main():
    customers = mk_customers(500)
    products = mk_products()
    proposals = mk_proposals(customers, products, n=800)
    contracts = mk_contracts(proposals)
    payments = mk_payments(contracts)
    transactions = mk_transactions(customers, n=2000)

    customers.to_csv(os.path.join(OUT, 'customers.csv'), index=False)
    products.to_csv(os.path.join(OUT, 'products.csv'), index=False)
    proposals.to_csv(os.path.join(OUT, 'proposals.csv'), index=False)
    contracts.to_csv(os.path.join(OUT, 'contracts.csv'), index=False)
    payments.to_csv(os.path.join(OUT, 'payments.csv'), index=False)
    transactions.to_csv(os.path.join(OUT, 'transactions.csv'), index=False)

    print('Generated CSVs in', OUT)


if __name__ == '__main__':
    main()
