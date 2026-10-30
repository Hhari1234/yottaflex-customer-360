import re
from typing import Optional


def normalize_email(email: Optional[str]) -> Optional[str]:
    if email is None or (isinstance(email, float) and str(email) == 'nan'):
        return None
    email_str = str(email).strip().lower()
    # Basic normalization
    return email_str if email_str else None


def normalize_phone(phone: Optional[str]) -> Optional[str]:
    if phone is None or (isinstance(phone, float) and str(phone) == 'nan'):
        return None
    phone_str = str(phone)
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone_str)
    return digits if digits else None


def is_valid_email(email: Optional[str]) -> bool:
    if email is None:
        return False
    normalized = normalize_email(email)
    if not normalized:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, normalized))
