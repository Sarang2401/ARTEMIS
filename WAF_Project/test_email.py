# test_email.py
import os
import sys

# Print current directory for debugging
print(f"Current directory: {os.getcwd()}")
print(f"Files in directory: {os.listdir('.')}")

# Add more verbose error handling
try:
    from email_alerts import send_alert_email
    print("Successfully imported send_alert_email function")
except ImportError as e:
    print(f"Import error: {e}")
    if os.path.exists("email_alerts.py"):
        print("The file email_alerts.py exists but might have issues")
        with open("email_alerts.py", "r") as f:
            content = f.read()
            print("Content of email_alerts.py:")
            print("-" * 50)
            print(content)
            print("-" * 50)
    else:
        print("The file email_alerts.py does not exist in this directory")
    sys.exit(1)

import logging

# Set up basic logging for test
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def test_email_alert():
    """Test the email alert functionality"""
    print("Sending test security alert email...")
    result = send_alert_email(
        attack_type="Test Alert", 
        payload="This is a test payload", 
        ip_address="127.0.0.1", 
        user_agent="Test User Agent"
    )
    if result:
        print("Test email sent successfully! Please check the receiver's inbox.")
    else:
        print("Failed to send test email. Check the logs for errors.")

if __name__ == "__main__":
    test_email_alert()