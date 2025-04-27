# waf.py
import re
import logging
from email_alerts import send_alert_email

# SQL injection patterns
sql_injection_patterns = [
    r"(?i)(\b(select|update|union|insert|delete|drop|alter)\b.*\bfrom\b)",
    r"(?i)(\b(or|and)\b\s+\w+\s*=\s*\w+)",
    r"(?i)(--|\#|\*|;)",
    r"(?i)('|\")\s*or\s*('|\")\s*=\s*('|\")",
    r"(?i)(\b(exec|execute|xp_cmdshell)\b)"
]

# XSS patterns
xss_patterns = [
    r"(?i)(<script>|<\/script>)",
    r"(?i)(javascript:)",
    r"(?i)(onload=|onerror=|onmouseover=|onclick=|onmouseout=)",
    r"(?i)(alert\(|prompt\(|confirm\()",
    r"(?i)(<img[^>]+src[^>]*>)"
]

def check_for_attacks(user_input, request):
    """Check if the user input contains SQL injection or XSS attacks"""
    
    # Get client info for the alert
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    # Check for SQL injection
    for pattern in sql_injection_patterns:
        if re.search(pattern, user_input):
            logging.warning(f"SQL injection attempt detected: {user_input} from {ip_address}")
            send_alert_email("SQL Injection", user_input, ip_address, user_agent)
            return True, "SQL Injection"
    
    # Check for XSS
    for pattern in xss_patterns:
        if re.search(pattern, user_input):
            logging.warning(f"XSS attempt detected: {user_input} from {ip_address}")
            send_alert_email("Cross-Site Scripting (XSS)", user_input, ip_address, user_agent)
            return True, "XSS"
    
    return False, None