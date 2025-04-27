# email_alerts.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from datetime import datetime
import os

def load_config():
    """Simple direct config loader for testing"""
    import configparser
    config = configparser.ConfigParser()
    config_path = os.path.join(os.getcwd(), 'config.ini')
    print(f"Loading config from: {config_path}")
    config.read(config_path)
    print(f"Config sections: {config.sections()}")
    return config

def send_alert_email(attack_type, payload, ip_address, user_agent):
    """Send an email alert when a potential attack is detected"""
    
    try:
        # Load email configuration directly for testing
        config = load_config()
        
        # Check if EMAIL section exists
        if 'EMAIL' not in config:
            print("ERROR: 'EMAIL' section not found in config.ini")
            print(f"Available sections: {config.sections()}")
            return False
        
        sender_email = config['EMAIL']['sender_email']
        receiver_email = config['EMAIL']['receiver_email']
        password = config['EMAIL']['password']
        smtp_server = config['EMAIL']['smtp_server']
        port = int(config['EMAIL']['port'])
        
        # Create message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = f"SECURITY ALERT: {attack_type} Attempt Detected!"
        
        # Email body
        body = f"""
        Security Alert: {attack_type} Attack Detected
        
        Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        Attack Type: {attack_type}
        Payload: {payload}
        IP Address: {ip_address}
        User Agent: {user_agent}
        
        This is an automated security alert.
        """
        
        message.attach(MIMEText(body, "plain"))
        
        print(f"Attempting to send email from {sender_email} to {receiver_email} via {smtp_server}:{port}")
        
        # Create SMTP session
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        
        # Send email
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        logging.info(f"Email alert sent: {attack_type} from {ip_address}")
        return True
    except Exception as e:
        logging.error(f"Failed to send email alert: {str(e)}")
        print(f"Error sending email: {str(e)}")
        return False