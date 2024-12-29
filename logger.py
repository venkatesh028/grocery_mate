# logger.py
import logging
from logging.handlers import RotatingFileHandler


def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Change to INFO in production

    log_format = '[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s'
    formatter = logging.Formatter(log_format)

    # Console handler (prints logs to the console)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (writes logs to a file with rotation)
    log_file = 'app.log'
    file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
