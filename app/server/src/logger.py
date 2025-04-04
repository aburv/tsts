"""
Logging module
"""
import logging


class LoggerAPI:
    """
     logger class
     helps with logging
    """

    def __init__(self) -> None:
        logging.basicConfig(level="INFO")
        self.logger = logging.getLogger(__name__)

    def info_entry(self, message) -> None:
        """
        :param message:
        :type message:
        :return:
        :rtype:
        """
        self.logger.info(message)

    def error_entry(self, message) -> None:
        """
        :param message:
        :type message:
        :return:
        :rtype:
        """
        self.logger.error(message)

    def warning_entry(self, message) -> None:
        """
        :param message:
        :type message:
        :return:
        :rtype:
        """
        self.logger.warning(message)