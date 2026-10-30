import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os
from pathlib import Path


class DataGenerator:
    def __init__(self, seed: int = 42):
        self.seed = seed
        random.seed(seed)
        Faker.seed(seed)
        self.fake = Faker()
        
    def generate_customers(self, n: int = 100) -> pd.DataFrame:
        customers = []
        customer_ids = []
        
        for i in range(1, n + 1):
            cust_id = f'CUST{i:08d}'
            customer_ids.append(cust_id)
            email = self.fake.email() if random.random() > 0.05 else None
            phone = self.fake.phone_number() if random.random() > 0.05 else None
            customers.append({
                'customer_id': cust_id,
                'first_name': self.fake.first_name(),
                'last_name': self.fake.last_name(),
                'email': email,
                'phone': phone,
                'address': self.fake.address().replace('\n', ', '),
                'date_of_birth': self.fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%Y-%m-%d'),
                'created_at': self.fake.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
            })
        
        duplicates = []
        for i in range(min(10, n)):
            orig = customers[i].copy()
            dup = orig.copy()
            dup['customer_id'] = f'CUST{n + i + 100:08d}'
            if dup['phone'] and random.random() > 0.5:
                dup['phone'] = self.fake.phone_number()
            duplicates.append(dup)
        
        df = pd.DataFrame(customers + duplicates)
        return df
    
    def generate_accounts(self, customers_df: pd.DataFrame, n_accounts: int = 150) -> pd.DataFrame:
        accounts = []
        customer_ids = customers_df['customer_id'].tolist()
        
        for i in range(1, n_accounts + 1):
            acc_id = f'ACC{i:08d}'
            if random.random() > 0.02:
                cust_id = random.choice(customer_ids)
            else:
                cust_id = f'CUST{99999999}'
            accounts.append({
                'account_id': acc_id,
                'customer_id': cust_id,
                'account_type': random.choice(['checking', 'savings', 'credit', 'loan']),
                'account_status': random.choice(['active', 'inactive', 'suspended']),
                'balance': round(random.uniform(0, 10000), 2),
                'opened_date': self.fake.date_between(start_date='-3y', end_date='now').strftime('%Y-%m-%d'),
                'created_at': self.fake.date_time_between(start_date='-3y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
            })
        return pd.DataFrame(accounts)
    
    def generate_orders(self, customers_df: pd.DataFrame, n_orders: int = 300) -> pd.DataFrame:
        orders = []
        customer_ids = customers_df['customer_id'].tolist()
        
        for i in range(1, n_orders + 1):
            ord_id = f'ORD{i:08d}'
            if random.random() > 0.02:
                cust_id = random.choice(customer_ids)
            else:
                cust_id = f'CUST{88888888}'
            orders.append({
                'order_id': ord_id,
                'customer_id': cust_id,
                'order_date': self.fake.date_time_between(start_date='-1y', end_date='now').strftime('%Y-%m-%d %H:%M:%S'),
                'order_status': random.choice(['completed', 'pending', 'cancelled', 'refunded']),
                'total_amount': round(random.uniform(10, 1000), 2),
                'payment_method': random.choice(['credit_card', 'debit_card', 'paypal', 'cash']),
                'created_at': self.fake.date_time_between(start_date='-1y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
            })
        return pd.DataFrame(orders)
    
    def generate_interactions(self, customers_df: pd.DataFrame, n_interactions: int = 400) -> pd.DataFrame:
        interactions = []
        customer_ids = customers_df['customer_id'].tolist()
        
        for i in range(1, n_interactions + 1):
            int_id = f'INT{i:08d}'
            if random.random() > 0.02:
                cust_id = random.choice(customer_ids)
            else:
                cust_id = f'CUST{77777777}'
            interactions.append({
                'interaction_id': int_id,
                'customer_id': cust_id,
                'interaction_type': random.choice(['call', 'email', 'chat', 'in_person']),
                'interaction_date': self.fake.date_time_between(start_date='-1y', end_date='now').strftime('%Y-%m-%d %H:%M:%S'),
                'agent_id': f'AGENT{random.randint(1, 20):03d}',
                'notes': self.fake.sentence()[:100],
                'created_at': self.fake.date_time_between(start_date='-1y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
            })
        return pd.DataFrame(interactions)

