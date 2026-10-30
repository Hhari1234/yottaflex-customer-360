import pandas as pd
import re
from typing import Dict, List, Tuple
from src.utils.validation_utils import is_valid_email, normalize_email, normalize_phone


class DataValidator:
    def __init__(self, logger=None):
        self.logger = logger or __import__('logging').getLogger('yottaflex_pipeline')
        self.rejected_records = []
        
    def validate_customers(self, df: pd.DataFrame, run_id: str, source_file: str) -> Tuple[pd.DataFrame, List[Dict]]:
        valid_rows = []
        rejected = []
        
        required = ['customer_id', 'first_name', 'last_name']
        
        for idx, row in df.iterrows():
            reasons = []
            # Check required
            for req in required:
                if req not in df.columns or pd.isna(row.get(req)) or str(row.get(req)).strip() == '':
                    reasons.append(f'Missing required field: {req}')
            
            # Check email format if present
            if 'email' in df.columns and pd.notna(row.get('email')):
                if not is_valid_email(row.get('email')):
                    reasons.append('Invalid email format')
            
            if reasons:
                rejected.append({
                    'source_dataset': 'customers',
                    'source_file': source_file,
                    'original_index': idx,
                    'record_data': str(row.to_dict()),
                    'rejection_reason': '; '.join(reasons),
                    'run_id': run_id
                })
            else:
                valid_rows.append(idx)
        
        valid_df = df.loc[valid_rows].copy()
        self.rejected_records.extend(rejected)
        return valid_df, rejected
    
    def validate_accounts(self, df: pd.DataFrame, run_id: str, source_file: str) -> Tuple[pd.DataFrame, List[Dict]]:
        valid_rows = []
        rejected = []
        required = ['account_id', 'customer_id']
        
        for idx, row in df.iterrows():
            reasons = []
            for req in required:
                if req not in df.columns or pd.isna(row.get(req)) or str(row.get(req)).strip() == '':
                    reasons.append(f'Missing required field: {req}')
            if reasons:
                rejected.append({
                    'source_dataset': 'accounts',
                    'source_file': source_file,
                    'original_index': idx,
                    'record_data': str(row.to_dict()),
                    'rejection_reason': '; '.join(reasons),
                    'run_id': run_id
                })
            else:
                valid_rows.append(idx)
        
        valid_df = df.loc[valid_rows].copy()
        self.rejected_records.extend(rejected)
        return valid_df, rejected
    
    def validate_orders(self, df: pd.DataFrame, run_id: str, source_file: str) -> Tuple[pd.DataFrame, List[Dict]]:
        valid_rows = []
        rejected = []
        required = ['order_id', 'customer_id']
        
        for idx, row in df.iterrows():
            reasons = []
            for req in required:
                if req not in df.columns or pd.isna(row.get(req)) or str(row.get(req)).strip() == '':
                    reasons.append(f'Missing required field: {req}')
            if reasons:
                rejected.append({
                    'source_dataset': 'orders',
                    'source_file': source_file,
                    'original_index': idx,
                    'record_data': str(row.to_dict()),
                    'rejection_reason': '; '.join(reasons),
                    'run_id': run_id
                })
            else:
                valid_rows.append(idx)
        
        valid_df = df.loc[valid_rows].copy()
        self.rejected_records.extend(rejected)
        return valid_df, rejected
    
    def validate_interactions(self, df: pd.DataFrame, run_id: str, source_file: str) -> Tuple[pd.DataFrame, List[Dict]]:
        valid_rows = []
        rejected = []
        required = ['interaction_id', 'customer_id']
        
        for idx, row in df.iterrows():
            reasons = []
            for req in required:
                if req not in df.columns or pd.isna(row.get(req)) or str(row.get(req)).strip() == '':
                    reasons.append(f'Missing required field: {req}')
            if reasons:
                rejected.append({
                    'source_dataset': 'interactions',
                    'source_file': source_file,
                    'original_index': idx,
                    'record_data': str(row.to_dict()),
                    'rejection_reason': '; '.join(reasons),
                    'run_id': run_id
                })
            else:
                valid_rows.append(idx)
        
        valid_df = df.loc[valid_rows].copy()
        self.rejected_records.extend(rejected)
        return valid_df, rejected

