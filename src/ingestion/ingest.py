import os
import pandas as pd
from pathlib import Path
from typing import Dict, Tuple
import logging


class DataIngestion:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger('yottaflex_pipeline')
        
    def read_csv(self, file_path: str, dataset_name: str) -> pd.DataFrame:
        try:
            if not os.path.exists(file_path):
                self.logger.error(f'File not found: {file_path}')
                raise FileNotFoundError(f'{dataset_name} file not found: {file_path}')
            
            df = pd.read_csv(file_path)
            self.logger.info(f'Read {len(df)} records from {file_path} for {dataset_name}')
            return df
        except Exception as e:
            self.logger.error(f'Error reading {dataset_name} from {file_path}: {str(e)}')
            raise
    
    def ingest_all(self, data_dir: str) -> Dict[str, pd.DataFrame]:
        data_path = Path(data_dir)
        result = {}
        
        for name in ['customers', 'accounts', 'orders', 'interactions']:
            file_path = data_path / f'{name}.csv'
            result[name] = self.read_csv(str(file_path), name)
        
        return result

