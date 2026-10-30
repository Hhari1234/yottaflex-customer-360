import os
import time
from datetime import datetime
from pathlib import Path
import pandas as pd

from src.ingestion.ingest import DataIngestion
from src.validation.validate import DataValidator
from src.matching.deduplication import CustomerMatcher
from src.transformation.unify import CustomerUnifier
from src.storage.db import DatabaseManager
from src.utils.ids import IDGenerator
from src.utils.logging import setup_logging


class PipelineOrchestrator:
    def __init__(self, data_dir='data/sample_small', output_dir='outputs'):
        self.data_dir = data_dir
        self.output_dir = output_dir
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        Path(os.path.join(output_dir, 'rejected')).mkdir(parents=True, exist_ok=True)
        Path('logs').mkdir(parents=True, exist_ok=True)
        self.logger = setup_logging()
        self.ingestion = DataIngestion(self.logger)
        self.validator = DataValidator(self.logger)
        self.matcher = CustomerMatcher(self.logger)
        self.unifier = CustomerUnifier(self.logger)
        self.id_gen = IDGenerator()
        
    def run(self):
        run_id = self.id_gen.generate_run_id()
        start_time = datetime.now()
        self.logger.info(f'Starting pipeline run: {run_id}')
        
        try:
            raw_data = self.ingestion.ingest_all(self.data_dir)
            input_counts = {k: len(v) for k,v in raw_data.items()}
            
            valid_customers, rej_cust = self.validator.validate_customers(
                raw_data['customers'], run_id, f'{self.data_dir}/customers.csv')
            valid_accounts, rej_acc = self.validator.validate_accounts(
                raw_data['accounts'], run_id, f'{self.data_dir}/accounts.csv')
            valid_orders, rej_ord = self.validator.validate_orders(
                raw_data['orders'], run_id, f'{self.data_dir}/orders.csv')
            valid_interactions, rej_int = self.validator.validate_interactions(
                raw_data['interactions'], run_id, f'{self.data_dir}/interactions.csv')
            
            all_rejected = rej_cust + rej_acc + rej_ord + rej_int
            
            deduped_customers, duplicates = self.matcher.deduplicate_customers(valid_customers, run_id)
            
            unified = self.unifier.create_unified_view(
                deduped_customers, valid_accounts, valid_orders, valid_interactions, run_id)
            
            unified.to_csv(os.path.join(self.output_dir, 'unified_customers.csv'), index=False)
            if all_rejected:
                pd.DataFrame(all_rejected).to_csv(
                    os.path.join(self.output_dir, 'rejected', f'rejected_{run_id}.csv'), index=False)
            
            db = DatabaseManager(os.path.join(self.output_dir, 'customer_360.db'))
            # Load only columns that exist
            customers_to_load = deduped_customers.copy()
            customers_to_load['run_id'] = run_id
            db.load_dataframe(customers_to_load, 'customers')
            valid_accounts['run_id'] = run_id
            db.load_dataframe(valid_accounts, 'accounts')
            valid_orders['run_id'] = run_id
            db.load_dataframe(valid_orders, 'orders')
            valid_interactions['run_id'] = run_id
            db.load_dataframe(valid_interactions, 'interactions')
            unified_out = unified.copy()
            unified_out['run_id'] = run_id
            db.load_dataframe(unified_out, 'unified_customers')
            if all_rejected:
                rej_df = pd.DataFrame(all_rejected)
                db.load_dataframe(rej_df, 'rejected_records')
            if not duplicates.empty:
                dup_df = duplicates[['customer_id', 'unified_customer_id']].copy()
                dup_df['match_reason'] = 'normalized_email_match'
                dup_df['confidence'] = 'high'
                dup_df['run_id'] = run_id
                db.load_dataframe(dup_df, 'uncertain_customer_matches')
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            run_stats = {
                'run_id': run_id,
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'duration_seconds': duration,
                'status': 'success',
                'input_customers': input_counts['customers'],
                'input_accounts': input_counts['accounts'],
                'input_orders': input_counts['orders'],
                'input_interactions': input_counts['interactions'],
                'processed_records': len(deduped_customers) + len(valid_accounts) + len(valid_orders) + len(valid_interactions),
                'rejected_records': len(all_rejected),
                'output_records': len(unified),
                'duplicates_found': len(duplicates),
                'failure_reason': None
            }
            
            db.load_dataframe(pd.DataFrame([run_stats]), 'pipeline_runs')
            db.close()
            
            self.logger.info(f'Pipeline completed successfully. Output: {len(unified)} unified customers')
            print(f'Run {run_id} completed in {duration:.2f}s. Unified customers: {len(unified)}, Rejected: {len(all_rejected)}, Duplicates: {len(duplicates)}')
            return run_stats
            
        except Exception as e:
            self.logger.error(f'Pipeline failed: {str(e)}', exc_info=True)
            raise

