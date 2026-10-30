import pandas as pd
from src.transformation.unify import CustomerUnifier
customers = pd.DataFrame({
    'customer_id': ['C1'],
    'first_name': ['John'],
    'last_name': ['Doe'],
    'email': ['john@test.com'],
    'phone': ['1234567890'],
    'norm_email': ['john@test.com'],
    'norm_phone': ['1234567890'],
    'unified_customer_id': ['C1']
})
accounts = pd.DataFrame({
    'account_id': ['A1', 'A2'],
    'customer_id': ['C1', 'C1'],
    'account_type': ['checking', 'savings']
})
orders = pd.DataFrame({
    'order_id': ['O1'],
    'customer_id': ['C1'],
    'order_date': ['2023-01-01 10:00:00'],
    'total_amount': [100.50]
})
interactions = pd.DataFrame({
    'interaction_id': ['I1', 'I2'],
    'customer_id': ['C1'],
    'interaction_date': ['2023-01-02 10:00:00']
})
unifier = CustomerUnifier()
unified = unifier.create_unified_view(customers, accounts, orders, interactions, 'RUN_TEST')
print(unified)

