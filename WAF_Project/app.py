# app.py
from flask import Flask, request, render_template, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import os

# Import from local modules
from waf import check_for_attacks
from utils.config_loader import load_config

# Set up the application
app = Flask(__name__)
config = load_config()

# Configure logging
log_directory = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_directory, exist_ok=True)
log_file = os.path.join(log_directory, 'waf.log')

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Set up rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def index():
    result = None
    attack_detected = False
    attack_type = None
    
    if request.method == 'POST':
        user_input = request.form.get('user_input', '')
        attack_detected, attack_type = check_for_attacks(user_input, request)
        
        if attack_detected:
            # Log attack and abort with 403 Forbidden
            return f"Security Alert: Potential {attack_type} detected", 403
        
        # Process the safe input
        result = f"Your input was processed: {user_input}"
    
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)