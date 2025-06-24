import re

def is_valid_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return re.match(pattern, email) is not None

def is_valid_phone(phone: str) -> bool:
    pattern = r"^\+?\d{10,15}$"
    return re.match(pattern, phone) is not None 