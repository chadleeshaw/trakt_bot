import logging
from os import environ as env


def my_logger(name: str) -> logging.Logger:
    log_level = env.get('LOG_LEVEL', 'INFO')

    logger = logging.getLogger(name)
    if not logger.handlers:
        console_formatter = logging.Formatter('%(asctime)s~%(levelname)s -- %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    logger.setLevel(log_level)

    return logger
