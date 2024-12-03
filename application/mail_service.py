from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# SMTP configuration
SMTP_HOST = "localhost"  # SMTP server host
SMTP_PORT = 1025         # SMTP server port (use the appropriate port)
SENDER_EMAIL = "princessant89@gmail.com"  # Replace with a valid email address
SENDER_PASSWORD = ""     # Update if password authentication is required

def send_message(to, subject, content_body):
    """
    Sends an email to the specified recipient.

    Parameters:
        to (str): Recipient's email address.
        subject (str): Subject of the email.
        content_body (str): HTML content of the email body.
    """
    # Create a MIME multipart message
    msg = MIMEMultipart()
    msg["To"] = to
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL

    # Attach the email body as HTML
    msg.attach(MIMEText(content_body, 'html'))

    # Connect to the SMTP server and send the message
    try:
        client = SMTP(host=SMTP_HOST, port=SMTP_PORT)
        client.send_message(msg=msg)
        client.quit()
        print(f"Email successfully sent to {to}")
    except Exception as e:
        print(f"Failed to send email to {to}. Error: {e}")
