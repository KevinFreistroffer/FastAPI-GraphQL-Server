import json
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(event, context):
    try:
        # Parse event data
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        user = body['user']
        recipient_email = body['email']
        
        # Email settings
        SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
        SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
        SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD')  # App password for Gmail
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Welcome to Our App!"
        msg['From'] = f"Your App <{SENDER_EMAIL}>"
        msg['To'] = recipient_email

        # Create text and HTML versions
        text_content = f"Hi {user['name']},\n\nWelcome to our app!"
        html_content = f"""
            <html>
            <head></head>
            <body>
                <h1>Welcome to Our App!</h1>
                <p>Hi {user['name']},</p>
                <p>Thank you for joining our app!</p>
            </body>
            </html>
        """

        # Attach both versions
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        msg.attach(part1)
        msg.attach(part2)

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Enable TLS
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Email sent successfully",
                "recipient": recipient_email
            })
        }
        
    except smtplib.SMTPException as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": f"SMTP error: {str(e)}"
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": f"Unexpected error: {str(e)}"
            })
        }
