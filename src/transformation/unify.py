import pandas as pd
from typing import Dict
from datetime import datetime


class CustomerUnifier:
    def __init__(self, logger=None):
        self.logger = logger or __import__('logging').getLogger('yottaflex_pipeline')
        
    def create_unified_view(self, customers_df: pd.DataFrame, accounts_df: pd.DataFrame, 
                           orders_df: pd.DataFrame, interactions_df: pd.DataFrame,
                           run_id: str) -> pd.DataFrame:
        # Aggregate accounts
        accounts_agg = accounts_df.groupby('customer_id').agg(
            account_count=('account_id', 'count'),
            account_types=('account_type', lambda x: ','.join(sorted(set(str(a) for a in x.unique() if pd.notna(a)))))
        ).reset_index()
        
        # Aggregate orders
        orders_agg = orders_df.groupby('customer_id').agg(
            total_orders=('order_id', 'count'),
            total_order_amount=('total_amount', 'sum'),
            last_order_date=('order_date', 'max')
        ).reset_index()
        
        # Aggregate interactions
        interactions_agg = interactions_df.groupby('customer_id').agg(
            interaction_count=('interaction_id', 'count'),
            last_interaction_date=('interaction_date', 'max')
        ).reset_index()
        
        unified = customers_df.copy()
        
        unified = unified.merge(accounts_agg.rename(columns={'customer_id': 'orig_cust'}), 
                               left_on='customer_id', right_on='orig_cust', how='left')
        unified = unified.merge(orders_agg.rename(columns={'customer_id': 'orig_cust2'}), 
                               left_on='customer_id', right_on='orig_cust2', how='left')
        unified = unified.merge(interactions_agg.rename(columns={'customer_id': 'orig_cust3'}), 
                               left_on='customer_id', right_on='orig_cust3', how='left')
        
        unified['account_count'] = unified['account_count'].fillna(0).astype(int)
        unified['total_orders'] = unified['total_orders'].fillna(0).astype(int)
        unified['total_order_amount'] = unified['total_order_amount'].fillna(0.0)
        unified['interaction_count'] = unified['interaction_count'].fillna(0).astype(int)
        unified['account_types'] = unified['account_types'].fillna('')
        unified['last_order_date'] = unified['last_order_date'].fillna('')
        unified['last_interaction_date'] = unified['last_interaction_date'].fillna('')
        
        agg_dict = {
            'first_name': 'first',
            'last_name': 'first',
            'email': 'first',
            'phone': 'first',
            'norm_email': 'first',
            'norm_phone': 'first',
            'account_count': 'sum',
            'total_orders': 'sum',
            'total_order_amount': 'sum',
            'interaction_count': 'sum',
            'last_order_date': 'max',
            'last_interaction_date': 'max',
            'account_types': lambda x: ','.join(sorted(set([str(a) for a in x if pd.notna(a) and a != '']))),
            'customer_id': lambda x: '|'.join(sorted(set(str(c) for c in x)))
        }
        
        unified_grouped = unified.groupby('unified_customer_id').agg(agg_dict).reset_index()
        unified_grouped = unified_grouped.rename(columns={'customer_id': 'source_record_ids'})
        unified_grouped['run_id'] = run_id
        unified_grouped['data_quality_status'] = 'valid'
        
        return unified_grouped

