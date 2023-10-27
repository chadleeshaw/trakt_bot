import logging
from os import environ as env

def my_logger(name: str) -> logging:
    log_level = env.get('LOG_LEVEL', 'INFO')

    console_formatter = logging.Formatter('%(asctime)s~%(levelname)s -- %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)

    logger = logging.getLogger(name)
    logger.addHandler(console_handler)
    logger.setLevel(log_level)
    
    return logger