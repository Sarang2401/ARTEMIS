# utils/validators.py
import re

def is_valid_input(input_str, max_length=500):
    """
    Perform basic input validation
    Returns True if input is valid, False otherwise
    """
    if not input_str or len(input_str) > max_length:
        return False
    
    # Example of additional validation rules
    # Prevent command injections
    dangerous_chars = r'[;&|`]'
    if re.search(dangerous_chars, input_str):
        return False
        
    return True