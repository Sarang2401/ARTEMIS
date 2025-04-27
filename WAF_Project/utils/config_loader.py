# utils/config_loader.py
import configparser
import os

def load_config():
    """Load configuration from config.ini file"""
    config = configparser.ConfigParser()
    
    # Use absolute path to the config file
    config_path = os.path.join(os.getcwd(), 'config.ini')
    
    print(f"Looking for config file at: {config_path}")
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at {config_path}")
    
    # Read the config file
    config.read(config_path)
    
    # Debug: Print available sections
    print(f"Config sections found: {config.sections()}")
    
    return config