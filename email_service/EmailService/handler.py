import json
import boto3
from botocore.exceptions import ClientError

def send_email(event, context):
    try:
        # Parse event data
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        user = body['user']
        email = body['email']
        
        # Create SES client
        ses = boto3.client('ses')
        
        # Prepare email
        SENDER = "Your App <noreply@yourdomain.com>"
        RECIPIENT = email
        SUBJECT = "Welcome to Our App!"
        BODY_TEXT = f"Hi {user['name']},\n\nWelcome to our app!"
        BODY_HTML = f"""
            <html>
            <head></head>
            <body>
                <h1>Welcome to Our App!</h1>
                <p>Hi {user['name']},</p>
                <p>Thank you for joining our app!</p>
            </body>
            </html>
        """

        # Send email
        response = ses.send_email(
            Source=SENDER,
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ]
            },
            Message={
                'Subject': {
                    'Data': SUBJECT
                },
                'Body': {
                    'Text': {
                        'Data': BODY_TEXT
                    },
                    'Html': {
                        'Data': BODY_HTML
                    }
                }
            }
        )
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Email sent successfully",
                "messageId": response['MessageId']
            })
        }
        
    except ClientError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": f"Email failed to send: {str(e)}"
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": f"Unexpected error: {str(e)}"
            })
        }
