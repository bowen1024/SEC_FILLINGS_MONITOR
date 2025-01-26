import smtplib
from email.mime.text import MIMEText
import logging
from sec_monitor.config import config

def send_notification(subject, body, is_critical=True):
    if not config.email_config.get('smtp_server'):
        logging.warning("Email not configured, skipping notification")
        return

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = config.email_config['email_user']
    if is_critical:
        msg['To'] = config.email_config['recipient']
    else:
        msg['To'] = config.email_config['email_user']

    try:
        with smtplib.SMTP_SSL(
            config.email_config['smtp_server'],
            config.email_config['smtp_port']
        ) as server:
            server.login(
                config.email_config['email_user'],
                config.email_config['email_password']
            )
            server.send_message(msg)
        logging.info("Notification email sent")
    except Exception as e:
        logging.error(f"Email send failed: {e}")