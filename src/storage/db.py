import sqlite3
import pandas as pd
from pathlib import Path
from typing import Dict
import os


class DatabaseManager:
    def __init__(self, db_path: str = 'outputs/customer_360.db'):
        self.db_path = db_path
        Path(os.path.dirname(db_path)).mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
        
    def create_tables(self):
        cursor = self.conn.cursor()
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            date_of_birth TEXT,
            created_at TEXT,
            norm_email TEXT,
            norm_phone TEXT,
            unified_customer_id TEXT,
            run_id TEXT
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
            account_id TEXT PRIMARY KEY,
            customer_id TEXT,
            account_type TEXT,
            account_status TEXT,
            balance REAL,
            opened_date TEXT,
            created_at TEXT,
            run_id TEXT
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            customer_id TEXT,
            order_date TEXT,
            order_status TEXT,
            total_amount REAL,
            payment_method TEXT,
            created_at TEXT,
            run_id TEXT
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS interactions (
            interaction_id TEXT PRIMARY KEY,
            customer_id TEXT,
            interaction_type TEXT,
            interaction_date TEXT,
            agent_id TEXT,
            notes TEXT,
            created_at TEXT,
            run_id TEXT
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS unified_customers (
            unified_customer_id TEXT PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            phone TEXT,
            norm_email TEXT,
            norm_phone TEXT,
            account_count INTEGER,
            total_orders INTEGER,
            total_order_amount REAL,
            interaction_count INTEGER,
            last_order_date TEXT,
            last_interaction_date TEXT,
            account_types TEXT,
            source_record_ids TEXT,
            data_quality_status TEXT,
            run_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS rejected_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_dataset TEXT,
            source_file TEXT,
            original_index INTEGER,
            record_data TEXT,
            rejection_reason TEXT,
            run_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS pipeline_runs (
            run_id TEXT PRIMARY KEY,
            start_time TIMESTAMP,
            end_time TIMESTAMP,
            duration_seconds REAL,
            status TEXT,
            input_customers INTEGER,
            input_accounts INTEGER,
            input_orders INTEGER,
            input_interactions INTEGER,
            processed_records INTEGER,
            rejected_records INTEGER,
            output_records INTEGER,
            duplicates_found INTEGER,
            failure_reason TEXT
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS uncertain_customer_matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT,
            unified_customer_id TEXT,
            match_reason TEXT,
            confidence TEXT,
            run_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        self.conn.commit()
        
    def load_dataframe(self, df: pd.DataFrame, table_name: str, if_exists: str = 'append'):
        df.to_sql(table_name, self.conn, if_exists=if_exists, index=False)
        
    def execute_query(self, query: str) -> pd.DataFrame:
        return pd.read_sql_query(query, self.conn)
        
    def close(self):
        self.conn.close()

