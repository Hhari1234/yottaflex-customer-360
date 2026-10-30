import pytest
import os
import sys
from pathlib import Path
import pandas as pd
import tempfile
import shutil

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.data_generator import DataGenerator
from src.ingestion.ingest import DataIngestion
from src.validation.validate import DataValidator
from src.matching.deduplication import CustomerMatcher
from src.transformation.unify import CustomerUnifier


class TestPipeline:
    def setup_method(self):
        self.gen = DataGenerator(seed=42)
        self.temp_dir = tempfile.mkdtemp()
        
    def teardown_method(self):
        shutil.rmtree(self.temp_dir)
    
    def test_data_generation(self):
        customers = self.gen.generate_customers(10)
        assert len(customers) >= 10
        assert 'customer_id' in customers.columns
    
    def test_ingestion(self):
        gen = DataGenerator(seed=123)
        customers = gen.generate_customers(20)
        data_dir = Path(self.temp_dir) / 'data'
        data_dir.mkdir()
        customers.to_csv(data_dir / 'customers.csv', index=False)
        gen2 = DataGenerator(seed=124)
        accounts = gen2.generate_accounts(customers, 30)
        accounts.to_csv(data_dir / 'accounts.csv', index=False)
        gen3 = DataGenerator(seed=125)
        orders = gen3.generate_orders(customers, 40)
        orders.to_csv(data_dir / 'orders.csv', index=False)
        gen4 = DataGenerator(seed=126)
        interactions = gen4.generate_interactions(customers, 50)
        interactions.to_csv(data_dir / 'interactions.csv', index=False)
        
        ingestion = DataIngestion()
        data = ingestion.ingest_all(str(data_dir))
        assert 'customers' in data
        assert len(data['customers']) >= 20
    
    def test_validation(self):
        validator = DataValidator()
        df = pd.DataFrame({
            'customer_id': ['C1', 'C2', 'C3'],
            'first_name': ['John', 'Jane', 'Bob'],
            'last_name': ['Doe', 'Smith', 'Jones'],
            'email': ['john@test.com', 'invalid-email', 'bob@test.com']
        })
        valid, rejected = validator.validate_customers(df, 'RUN_TEST', 'test.csv')
        assert len(valid) == 2
        assert len(rejected) >= 1
    
    def test_deduplication(self):
        matcher = CustomerMatcher()
        df = pd.DataFrame({
            'customer_id': ['C1', 'C2', 'C3'],
            'first_name': ['John', 'John', 'Bob'],
            'last_name': ['Doe', 'Doe', 'Smith'],
            'email': ['john@test.com', 'john@test.com', 'bob@test.com'],
            'phone': ['1234567890', '9876543210', '5555555555']
        })
        result, duplicates = matcher.deduplicate_customers(df, 'RUN_TEST')
        assert len(result) == 3
        assert result[result['customer_id']=='C1']['unified_customer_id'].values[0] == result[result['customer_id']=='C2']['unified_customer_id'].values[0]
    
    def test_unified_view(self):
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
            'account_id': ['A1'],
            'customer_id': ['C1'],
            'account_type': ['checking']
        })
        orders = pd.DataFrame({
            'order_id': ['O1'],
            'customer_id': ['C1'],
            'order_date': ['2023-01-01 10:00:00'],
            'total_amount': [100.50]
        })
        interactions = pd.DataFrame({
            'interaction_id': ['I1'],
            'customer_id': ['C1'],
            'interaction_date': ['2023-01-02 10:00:00']
        })
        unifier = CustomerUnifier()
        unified = unifier.create_unified_view(customers, accounts, orders, interactions, 'RUN_TEST')
        assert len(unified) == 1
        assert unified.iloc[0]['account_count'] == 1
        assert unified.iloc[0]['total_orders'] == 1
        assert unified.iloc[0]['total_order_amount'] == 100.50

