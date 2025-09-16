import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()

def send_email_with_attachment(subject, body, to_emails, attachment_path=None, attachment_bytes=None, attachment_filename=None, smtp_provider='gmail'):
    """
    Send an email with optional attachment using Gmail or custom SMTP (e.g., mail.krsnaa.in).
    - subject: Email subject
    - body: Email body (plain text)
    - to_emails: List of recipient emails
    - attachment_path: Path to file to attach (optional)
    - attachment_bytes: Bytes of file to attach (optional, takes precedence over attachment_path)
    - attachment_filename: Filename for attachment (required if using attachment_bytes)
    - smtp_provider: 'gmail' or 'krsnaa'
    """
    if smtp_provider == 'gmail':
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_user = os.getenv('GMAIL_USER')
        smtp_pass = os.getenv('GMAIL_PASS')
    elif smtp_provider == 'krsnaa':
        smtp_server = 'mail.krsnaa.in'
        smtp_port = 587
        smtp_user = os.getenv('KRSNAA_USER')
        smtp_pass = os.getenv('KRSNAA_PASS')
    else:
        raise ValueError('Unknown SMTP provider')

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = ', '.join(to_emails)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    if attachment_bytes and attachment_filename:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment_bytes)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{attachment_filename}"')
        msg.attach(part)
    elif attachment_path:
        filename = os.path.basename(attachment_path)
        with open(attachment_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
            msg.attach(part)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)

    return True
