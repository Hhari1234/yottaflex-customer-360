import random
from datetime import datetime
import uuid


class IDGenerator:
    def __init__(self, seed: int = 42):
        random.seed(seed)
    
    def generate_customer_id(self, index: int) -> str:
        return f"CUST{index:08d}"
    
    def generate_account_id(self, index: int) -> str:
        return f"ACC{index:08d}"
    
    def generate_order_id(self, index: int) -> str:
        return f"ORD{index:08d}"
    
    def generate_interaction_id(self, index: int) -> str:
        return f"INT{index:08d}"
    
    def generate_run_id(self) -> str:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"RUN_{ts}_{uuid.uuid4().hex[:8]}"
