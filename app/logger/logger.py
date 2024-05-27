import os
import logging
from logging.handlers import TimedRotatingFileHandler


def configure_logging(app):
    # Create the logs folder if it doesn't exist
    log_directory = "logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Base path for the log file
    log_file_path = os.path.join(log_directory, "log")

    # Remove all existing handlers from the application logger
    del app.logger.handlers[:]

    # Create and configure the console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levellevel)s - %(message)s')
    console_handler.setFormatter(console_formatter)

    # Filter to ensure that WARNING, ERROR, and CRITICAL appear on the console
    class WarningErrorCriticalFilter(logging.Filter):
        def filter(self, record):
            return record.levelno >= logging.WARNING

    console_handler.addFilter(WarningErrorCriticalFilter())

    # Create and configure the file handler with daily rotation
    file_handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1, backupCount=30)
    file_handler.suffix = "%Y_%m_%d"  # Date format for the file name, without .txt
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levellevel)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    # Add the configured handlers to the application logger
    app.logger.addHandler(console_handler)
    app.logger.addHandler(file_handler)

    # Set the application logger level to the lowest possible
    app.logger.setLevel(logging.DEBUG)

    # Disable propagation to prevent logs from being handled by other Flask loggers
    app.logger.propagate = False
