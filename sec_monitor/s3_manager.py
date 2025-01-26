# sec_monitor/s3_manager.py
import boto3
import json
import logging
from sec_monitor.config import config

logger = logging.getLogger(__name__)

class S3Manager:
    def __init__(self):
        self.client = boto3.client('s3', **config.aws_credentials)
        logger.debug("Initialized S3 client")

    def read_json(self, bucket, key):
        try:
            obj = self.client.get_object(Bucket=bucket, Key=key)
            logger.debug(f"Successfully read JSON from s3://{bucket}/{key}")
            return json.loads(obj['Body'].read())
        except self.client.exceptions.NoSuchKey:
            logger.info(f"JSON file not found at s3://{bucket}/{key}")
            return {}
        except Exception as e:
            logger.error(f"S3 JSON read error: {str(e)}", exc_info=True)
            return {}

    def write_json(self, bucket, key, data):
        try:
            self.client.put_object(
                Bucket=bucket,
                Key=key,
                Body=json.dumps(data)
            )
            logger.info(f"Successfully wrote JSON to s3://{bucket}/{key}")
        except Exception as e:
            logger.error(f"S3 JSON write error: {str(e)}", exc_info=True)
            raise

    def append_to_file(self, bucket, key, content):
        try:
            existing = self.read_file(bucket, key)
            self.write_file(bucket, key, existing + content)
            logger.debug(f"Appended content to s3://{bucket}/{key}")
        except Exception as e:
            logger.error(f"S3 append error: {str(e)}", exc_info=True)
            raise

    def read_file(self, bucket, key):
        try:
            obj = self.client.get_object(Bucket=bucket, Key=key)
            logger.debug(f"Successfully read file from s3://{bucket}/{key}")
            return obj['Body'].read().decode()
        except self.client.exceptions.NoSuchKey:
            logger.info(f"File not found at s3://{bucket}/{key}")
            return ''
        except Exception as e:
            logger.error(f"S3 file read error: {str(e)}", exc_info=True)
            return ''

    def write_file(self, bucket, key, content):
        try:
            self.client.put_object(
                Bucket=bucket,
                Key=key,
                Body=content.encode()
            )
            logger.info(f"Successfully wrote file to s3://{bucket}/{key}")
        except Exception as e:
            logger.error(f"S3 file write error: {str(e)}", exc_info=True)
            raise