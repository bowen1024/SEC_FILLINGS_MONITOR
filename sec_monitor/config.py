import os
from dotenv import load_dotenv  # Optional for local development
load_dotenv()

class Config:
    @property
    def s3_bucket(self):
        return os.getenv('S3_BUCKET')

    @property
    def aws_credentials(self):
        return {
            'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY')
        }

    @property
    def email_config(self):
        return {
            'smtp_server': os.getenv('SMTP_SERVER'),
            'smtp_port': int(os.getenv('SMTP_PORT', 465)),
            'email_user': os.getenv('EMAIL_USER'),
            'email_password': os.getenv('EMAIL_PASSWORD'),
            'recipient': os.getenv('EMAIL_RECIPIENT')
        }

config = Config()