import sys
import logging
import logging.handlers


def get_logger(name):
    logger = logging.Logger(name)

    format_str = "[%(asctime)s][%(name)s][%(levelname)s] - %(funcName)s:%(lineno)s - %(message)s"

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter(format_str))
    logger.addHandler(console_handler)

    file_handler = logging.handlers.TimedRotatingFileHandler("{}.log".format(name), when="midnight")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(format_str))
    logger.addHandler(file_handler)

    logger.setLevel(logging.DEBUG)
    return logger
