import logging
import os
import sys
from logging import handlers
root_dir = os.path.dirname(
    os.path.abspath(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


def create_logger(logger_name, stdout_handler=False):
    """
    Creates a logger with rotating file handler.
    Change stdout_handler = True, for adding STDOUT Handler as well.
    :param logger_name: logger name (eg, __name__)
    :param stdout_handler: Switch to turn on STDOUT handler
    :return: logger
    """
    log_dir = os.path.join(root_dir, "logs")
    if os.path.isdir(log_dir) is False:
        os.mkdir(log_dir)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    log_template = "%(asctime)s %(module)s %(levelname)s: %(message)s"
    formatter = logging.Formatter(log_template)

    # Logging - File Handler
    log_file_size_in_mb = 10
    count_of_backups = 5    # example.log example.log.1 example.log.2
    log_file_size_in_bytes = log_file_size_in_mb * 1024 * 1024
    log_filename = os.path.join(log_dir, logger_name) + '.log'
    file_handler = handlers.RotatingFileHandler(
        log_filename,
        maxBytes=log_file_size_in_bytes,
        backupCount=count_of_backups
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Logging - STDOUT Handler
    if stdout_handler:
        log_template = "[%(module)s %(levelname)s]: %(message)s"
        formatter = logging.Formatter(log_template)
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        logger.addHandler(stdout_handler)

    return logger
