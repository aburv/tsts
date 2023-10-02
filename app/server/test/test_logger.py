import logging
import unittest
from logging import Logger
from unittest import mock
from unittest.mock import MagicMock

from src.logger import LoggerAPI


class LoggerTest(unittest.TestCase):

    @mock.patch('logging.basicConfig')
    @mock.patch('logging.getLogger')
    def test_should_init_get_logger(self,
                                    mock_get_logger,
                                    mock_basic_config):
        mock_basic_config.return_value = None
        mock_get_logger.return_value = MagicMock(Logger)

        LoggerAPI()

        mock_get_logger.assert_called_with('src.logger')
        mock_basic_config.assert_called_once_with(level="INFO")

    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch.object(Logger, 'info')
    def test_should_log_info(self,
                             mock_info,
                             mock_init_logger):
        logger = LoggerAPI()
        logger.logger = logging.getLogger('src.logger')
        message = 'message'
        logger.info_entry(message)

        mock_info.assert_called_once_with(message)
        mock_init_logger.assert_called_once_with()

    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch.object(Logger, 'error')
    def test_should_error_info(self,
                               mock_error,
                               mock_init_logger):
        message = 'message'

        logger = LoggerAPI()
        logger.logger = logging.getLogger('src.logger')
        logger.error_entry(message)

        mock_error.assert_called_once_with(message)
        mock_init_logger.assert_called_once_with()
