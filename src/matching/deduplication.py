import pandas as pd
from typing import Dict, List, Tuple
from src.utils.validation_utils import normalize_email, normalize_phone


class CustomerMatcher:
    def __init__(self, logger=None):
        self.logger = logger or __import__('logging').getLogger('yottaflex_pipeline')
        self.uncertain_matches = []
        
    def deduplicate_customers(self, df: pd.DataFrame, run_id: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        df_work = df.copy()
        df_work['norm_email'] = df_work['email'].apply(normalize_email)
        df_work['norm_phone'] = df_work['phone'].apply(normalize_phone)
        
        email_to_canonical = {}
        phone_to_canonical = {}
        canonical_map = {}
        used_as_canonical = set()
        
        for idx, row in df_work.iterrows():
            orig_id = row['customer_id']
            norm_email = row['norm_email']
            if norm_email and norm_email not in email_to_canonical:
                email_to_canonical[norm_email] = orig_id
                if orig_id not in used_as_canonical:
                    used_as_canonical.add(orig_id)
                    canonical_map[orig_id] = orig_id
        
        for idx, row in df_work.iterrows():
            orig_id = row['customer_id']
            norm_email = row['norm_email']
            if norm_email and norm_email in email_to_canonical:
                canonical = email_to_canonical[norm_email]
                canonical_map[orig_id] = canonical
        
        for idx, row in df_work.iterrows():
            orig_id = row['customer_id']
            if orig_id in canonical_map:
                continue
            norm_phone = row['norm_phone']
            if norm_phone and norm_phone in phone_to_canonical:
                canonical = phone_to_canonical[norm_phone]
                canonical_map[orig_id] = canonical
            elif norm_phone:
                phone_to_canonical[norm_phone] = orig_id
                canonical_map[orig_id] = orig_id
                used_as_canonical.add(orig_id)
            else:
                canonical_map[orig_id] = orig_id
        
        result = df_work.copy()
        result['unified_customer_id'] = result['customer_id'].map(canonical_map)
        
        duplicates = result[result['customer_id'] != result['unified_customer_id']].copy()
        duplicates['run_id'] = run_id
        
        uncertain_df = pd.DataFrame(self.uncertain_matches)
        return result, duplicates

