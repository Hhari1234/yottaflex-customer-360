import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.utils.data_generator import DataGenerator
import pandas as pd


def main():
    gen = DataGenerator(seed=42)
    customers = gen.generate_customers(50)
    accounts = gen.generate_accounts(customers, 75)
    orders = gen.generate_orders(customers, 150)
    interactions = gen.generate_interactions(customers, 200)
    
    data_dir = Path('data/sample_small')
    data_dir.mkdir(parents=True, exist_ok=True)
    
    customers.to_csv(data_dir / 'customers.csv', index=False)
    accounts.to_csv(data_dir / 'accounts.csv', index=False)
    orders.to_csv(data_dir / 'orders.csv', index=False)
    interactions.to_csv(data_dir / 'interactions.csv', index=False)
    
    print(f'Generated sample_small:')
    print(f'  Customers: {len(customers)}')
    print(f'  Accounts: {len(accounts)}')
    print(f'  Orders: {len(orders)}')
    print(f'  Interactions: {len(interactions)}')
    
    gen2 = DataGenerator(seed=123)
    customers_l = gen2.generate_customers(25000)
    accounts_l = gen2.generate_accounts(customers_l, 37500)
    orders_l = gen2.generate_orders(customers_l, 75000)
    interactions_l = gen2.generate_interactions(customers_l, 100000)
    
    data_dir_l = Path('data/sample_large')
    data_dir_l.mkdir(parents=True, exist_ok=True)
    
    customers_l.to_csv(data_dir_l / 'customers.csv', index=False)
    accounts_l.to_csv(data_dir_l / 'accounts.csv', index=False)
    orders_l.to_csv(data_dir_l / 'orders.csv', index=False)
    interactions_l.to_csv(data_dir_l / 'interactions.csv', index=False)
    
    print(f'\nGenerated sample_large:')
    print(f'  Customers: {len(customers_l)}')
    print(f'  Accounts: {len(accounts_l)}')
    print(f'  Orders: {len(orders_l)}')
    print(f'  Interactions: {len(interactions_l)}')


if __name__ == '__main__':
    main()

