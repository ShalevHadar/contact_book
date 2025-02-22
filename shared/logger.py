import logging
import sys

class AppLogger:
    def __init__(self, name: str = "contact_book_app_logger", level: int = logging.INFO):
        """
        Creates a logger with the given name and level. By default, logs at DEBUG level.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Prevent adding multiple handlers if logger already has them
        if not self.logger.handlers:
            # Create console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(level)

            # Create a formatter with timestamps, module name, log level, and the message
            formatter = logging.Formatter(
                fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            console_handler.setFormatter(formatter)

            # Add the handler to the logger
            self.logger.addHandler(console_handler)

    def info(self, message: str):
        self.logger.info(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def error(self, message: str, exc_info: bool = False):
        self.logger.error(message, exc_info=exc_info)

    def warning(self, message: str):
        self.logger.warning(message)

    def critical(self, message: str):
        self.logger.critical(message)

app_log = AppLogger(name="phonebook_app")