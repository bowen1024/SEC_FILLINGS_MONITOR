import logging
from sec_monitor.s3_manager import S3Manager
from sec_monitor.config import config


class S3LogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.buffer = []
        self.s3 = S3Manager()

    def emit(self, record):
        msg = self.format(record)
        self.buffer.append(msg)

    def flush(self):
        if self.buffer:
            logs = '\n'.join(self.buffer) + '\n'
            self.s3.append_to_file(config.s3_bucket, 'sec_fillings/logs.txt', logs)
            self.buffer = []


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Clear existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # S3 Handler
    s3_handler = S3LogHandler()
    formatter = logging.Formatter('%(asctime)sZ - %(levelname)s - %(message)s',
                                  '%Y-%m-%dT%H:%M:%S')
    s3_handler.setFormatter(formatter)
    logger.addHandler(s3_handler)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)