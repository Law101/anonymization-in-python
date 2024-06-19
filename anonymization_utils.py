import hashlib
import logging
import random
import string
from typing import Tuple, Dict, List


def generate_anonymized_value(value: str, salt: str, algorithm: str = 'sha256') -> str:
    '''
    Hashing function using SHA256
    '''
    hash_input = value + salt
    hash_func = getattr(hashlib, algorithm)
    return hash_func(hash_input.encode()).hexdigest()


def anonymize_column(column_values: List[str], salt: str) -> Tuple[List[str], Dict[str, str]]:
    '''
    Function for anonymizing each column
    '''
    try:
        unique_values = set(column_values)
        value_to_anonymize = {}
        for val in unique_values:
            anonymized_val = generate_anonymized_value(str(val), salt)
            # Checking and rehashing to ensure no hashing collisions
            while anonymized_val in value_to_anonymize.values():
                salt = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
                anonymized_val = generate_anonymized_value(str(val), salt)
            value_to_anonymize[val] = anonymized_val
        anonymized_column = [value_to_anonymize[val] for val in column_values]
        return anonymized_column, value_to_anonymize
    except Exception as e:
        logging.error(f"An error occurred during column anonymization: {e}")
        raise
