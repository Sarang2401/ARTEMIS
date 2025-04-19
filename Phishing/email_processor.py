import imaplib
import email
import time
import json
import requests
import smtplib
from email.message import EmailMessage
from email.header import decode_header

# --- CONFIGURATION ---
EMAIL_ADDRESS = " "        # Your Gmail address
EMAIL_PASSWORD = " "     # Gmail App Password (not your login password)
ALERT_RECEIVER = " "   # Where phishing alerts should be sent
IMAP_SERVER = "imap.gmail.com"
API_URL = "http://localhost:5000/predict"     # Flask prediction server

# --- ALERT FUNCTION ---
def send_alert_email(to_email, subject, probability, sender):
    msg = EmailMessage()
    msg['Subject'] = f"[PHISHING ALERT] {subject}"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email

    msg.set_content(f"""
    🚨 Potential Phishing Email Detected 🚨

    From: {sender}
    Subject: {subject}
    Phishing Probability: {probability:.2f}

    Please verify this email before taking any action.
    """)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"🔔 Alert sent to {to_email}")
    except Exception as e:
        print(f"⚠️ Error sending alert email: {e}")

# --- MAIN EMAIL PROCESSING ---
def process_emails(email_address, password, server=IMAP_SERVER):
    # Connect to email server
    mail = imaplib.IMAP4_SSL(server)
    mail.login(email_address, password)
    mail.select('inbox')

    print(f"📬 Monitoring inbox for {email_address}...")

    processed_ids = set()

    while True:
        status, email_ids = mail.search(None, 'UNSEEN')

        if status == 'OK':
            for email_id in email_ids[0].split():
                if email_id.decode() not in processed_ids:
                    status, email_data = mail.fetch(email_id, '(RFC822)')
                    raw_email = email_data[0][1]
                    msg = email.message_from_bytes(raw_email)

                    subject = decode_header(msg['Subject'])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(errors='ignore')

                    sender = msg['From']
                    body = ""

                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type in ['text/plain', 'text/html']:
                                try:
                                    body = part.get_payload(decode=True).decode(errors='ignore')
                                    break
                                except:
                                    pass
                    else:
                        body = msg.get_payload(decode=True).decode(errors='ignore')

                    email_data = {
                        'subject': subject,
                        'sender': sender,
                        'body': body
                    }

                    # --- Send data to prediction API ---
                    try:
                        response = requests.post(API_URL, json=email_data, timeout=10)
                        result = response.json()

                        print(f"\n📨 Email Subject: {subject}")
                        print(f"🧠 Phishing Probability: {result['probability']:.2f}")
                        print(f"🚫 Is Phishing: {'YES' if result['is_phishing'] else 'No'}")
                        print("-" * 50)

                        if result['is_phishing']:
                            send_alert_email(
                                to_email=ALERT_RECEIVER,
                                subject=subject,
                                probability=result['probability'],
                                sender=sender
                            )

                        processed_ids.add(email_id.decode())

                    except Exception as e:
                        print(f"⚠️ Error processing email: {str(e)}")

        time.sleep(60)  # Wait 1 min before checking again

# --- ENTRY POINT ---
if __name__ == "__main__":
    process_emails(EMAIL_ADDRESS, EMAIL_PASSWORD)
