import unittest
from unittest import mock

from flask import Flask

from src.logger import LoggerAPI
from src.responses import ValidResponse, SecurityException, TableNotFoundException, DBConnectionException, \
    DBExecutionException, DataValidationException, RuntimeException, CachedResponse, RecordNotFoundException


class ExceptionTest(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)

    @mock.patch.object(LoggerAPI, 'info_entry', return_value=None)
    def test_should_return_valid_response_with_context(self,
                                                       mock_info_entry):
        expected = b'{"data":"content"}\n'

        with self.app.app_context():
            actual = ValidResponse('message', 'content', detail='details').get_response_json()

        mock_info_entry.assert_called_once_with("Success message details : content")
        self.assertEqual(expected, actual.data)
        self.assertEqual(200, actual.status_code)

    @mock.patch.object(LoggerAPI, 'info_entry', return_value=None)
    def test_should_return_data_valid_response(self,
                                               mock_info_entry):
        with self.app.app_context():
            response = ValidResponse('message', 'content', detail='details')

        actual = response.get_data()

        mock_info_entry.assert_called_once_with("Success message details : content")
        self.assertEqual("content", actual)

    @mock.patch.object(LoggerAPI, 'info_entry', return_value=None)
    def test_should_return_cached_response_with_context(self,
                                                        mock_info_entry):
        expected = b'{"data":"content"}\n'

        with self.app.app_context():
            actual = CachedResponse(key='key', data='content').get_response_json()

        mock_info_entry.assert_called_once_with('Cached key : content')
        self.assertEqual(expected, actual.data)
        self.assertEqual(200, actual.status_code)

    @mock.patch.object(LoggerAPI, 'warning_entry', return_value=None)
    def test_should_return_auth_exception_with_context(self,
                                                       mock_warning_entry):
        expected = b'{"error":{"message":"message","type":"SecurityException"}}\n'

        with self.app.app_context():
            actual = SecurityException('message', 'content').get_response_json()

        mock_warning_entry.assert_called_once_with("401 SecurityException message : content")
        self.assertEqual(expected, actual.data)
        self.assertEqual(401, actual.status_code)

    @mock.patch.object(LoggerAPI, 'error_entry', return_value=None)
    def test_should_return_runtime_exception_with_context(self,
                                                          mock_error_entry):
        expected = b'{"error":{"message":"message","type":"RuntimeException"}}\n'

        with self.app.app_context():
            actual = RuntimeException('message', 'content').get_response_json()

        mock_error_entry.assert_called_once_with("500 RuntimeException message : content")
        self.assertEqual(expected, actual.data)
        self.assertEqual(500, actual.status_code)

    @mock.patch.object(LoggerAPI, 'warning_entry', return_value=None)
    def test_should_return_validation_exception_with_context(self,
                                                             mock_warning_entry):
        expected = b'{"error":{"message":"message","type":"DataValidationException"}}\n'

        with self.app.app_context():
            actual = DataValidationException('message', 'content').get_response_json()

        mock_warning_entry.assert_called_once_with("400 DataValidationException message : content")
        self.assertEqual(expected, actual.data)
        self.assertEqual(400, actual.status_code)

    @mock.patch.object(LoggerAPI, 'error_entry', return_value=None)
    def test_should_return_table_not_found_exception_with_context(self,
                                                                  mock_error_entry):
        expected = b'{"error":{"message":"","type":"TableNotFoundException"}}\n'

        with self.app.app_context():
            actual = TableNotFoundException('table').get_response_json()

        mock_error_entry.assert_called_once_with("2 TableNotFoundException  : table")
        self.assertEqual(expected, actual.data)
        self.assertEqual(500, actual.status_code)

    @mock.patch.object(LoggerAPI, 'error_entry', return_value=None)
    def test_should_return_db_connection_exception_with_context(self,
                                                                mock_error_entry):
        expected = b'{"error":{"message":"","type":"DBConnectionException"}}\n'

        with self.app.app_context():
            actual = DBConnectionException('message').get_response_json()

        mock_error_entry.assert_called_once_with("0 DBConnectionException  : message")
        self.assertEqual(expected, actual.data)
        self.assertEqual(500, actual.status_code)

    @mock.patch.object(LoggerAPI, 'error_entry', return_value=None)
    def test_should_return_db_execution_exception_with_context(self,
                                                               mock_error_entry):
        expected = b'{"error":{"message":"operation","type":"DBExecutionException"}}\n'

        with self.app.app_context():
            actual = DBExecutionException('operation', 'message').get_response_json()

        mock_error_entry.assert_called_once_with("1 DBExecutionException operation : message")
        self.assertEqual(expected, actual.data)
        self.assertEqual(500, actual.status_code)

    @mock.patch.object(LoggerAPI, 'error_entry', return_value=None)
    def test_should_return_the_record_not_found_exception_with_context(self,
                                                                       mock_error_entry):
        expected = b'{"error":{"message":"r_id","type":"RecordNotFoundException"}}\n'

        with self.app.app_context():
            actual = RecordNotFoundException('table', 'r_id').get_response_json()

        mock_error_entry.assert_called_once_with("404 RecordNotFoundException r_id : table")
        self.assertEqual(expected, actual.data)
        self.assertEqual(404, actual.status_code)
