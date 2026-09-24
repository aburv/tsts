import unittest
from unittest import mock

from flask import Flask, g

from src.logger import LoggerAPI
from src.responses import ValidResponse, SecurityException, TableNotFoundException, DBConnectionException, \
    DBExecutionException, DataValidationException, RuntimeException, CachedResponse, RecordNotFoundException, \
    get_turnaround_in_ms, APIException, APIResponse


class ExceptionTest(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)

    def test_should_return_APIResponse(self):
        actual = APIResponse('message')

        self.assertIsInstance(actual, APIResponse)
        self.assertEqual(actual.status_code, 200)
        self.assertEqual(actual.content, "message")

    def test_should_return_APIResponse_response(self):
        with mock.patch.object(APIResponse, '__init__', return_value=None):
            response = APIResponse('')
            response.status_code = 200
            response.content = "message"

        with self.app.app_context():
            actual = response.get_response_json()

        self.assertEqual(actual.status_code, 200)
        self.assertEqual(actual.data, b'{"data":"message"}\n')
        self.assertEqual(actual.headers['Content-Type'], "application/json")

    @mock.patch.object(LoggerAPI, 'info_entry', return_value=None)
    @mock.patch.object(APIResponse, '__init__', return_value=None)
    @mock.patch('src.responses.get_turnaround_in_ms', return_value=50)
    def test_should_return_valid_response_without_request_start_time(self,
                                                                     mock_get_turnaround_in_ms,
                                                                     mock_api,
                                                                     mock_info_entry):
        with self.app.app_context():
            g.request_id = "request_id"
            ValidResponse('message', 'content', detail='details')

        mock_api.assert_called_once_with('content')
        mock_info_entry.assert_called_once_with('request_id - 0 - 200 - Success message details : content')
        assert not mock_get_turnaround_in_ms.called

    @mock.patch.object(LoggerAPI, 'info_entry', return_value=None)
    @mock.patch.object(APIResponse, '__init__', return_value=None)
    @mock.patch('src.responses.get_turnaround_in_ms', return_value=50)
    def test_should_return_valid_response_with_request_start_time(self,
                                                                  mock_get_turnaround_in_ms,
                                                                  mock_api,
                                                                  mock_info_entry):
        with self.app.app_context():
            g.request_id = "request_id"
            g.start_time = 150.0
            ValidResponse('message', 'content', detail='details')

        mock_api.assert_called_once_with('content')
        mock_info_entry.assert_called_once_with('request_id - 50.0000 - 200 - Success message details : content')
        mock_get_turnaround_in_ms.assert_called_once_with(150.0)

    def test_should_return_data_valid_response(self):
        with self.app.app_context():
            with mock.patch.object(ValidResponse, '__init__', return_value=None):
                response = ValidResponse('message', 'content', detail='details')
                response.content = 'content'

        actual = response.get_data()

        self.assertEqual("content", actual)

    @mock.patch.object(LoggerAPI, 'info_entry', return_value=None)
    @mock.patch.object(APIResponse, '__init__', return_value=None)
    def test_should_return_cached_response(self,
                                           mock_api,
                                           mock_info_entry):
        actual = CachedResponse(key='key', data='content')

        self.assertIsInstance(actual, CachedResponse)
        mock_info_entry.assert_called_once_with('Cached key : content')
        mock_api.assert_called_once_with('content')

    @mock.patch.object(LoggerAPI, 'error_entry', return_value=None)
    @mock.patch('src.responses.get_turnaround_in_ms', return_value=50)
    def test_should_return_APIException_error_response_with_request_on_error(self,
                                                                             mock_get_turnaround_in_ms,
                                                                             mock_error_entry,
                                                                             ):
        with self.app.app_context():
            g.request_id = "request_id"
            actual = APIException('message', 'content', error_type="type", status_code=500, is_error=True)

        self.assertIsInstance(actual, APIException)
        mock_error_entry.assert_called_once_with('request_id - 0 - 500 type message : content')
        assert not mock_get_turnaround_in_ms.called

    @mock.patch.object(LoggerAPI, 'error_entry', return_value=None)
    @mock.patch('src.responses.get_turnaround_in_ms', return_value=50)
    def test_should_return_APIException_error_response_without_request_on_error(self,
                                                                                mock_get_turnaround_in_ms,
                                                                                mock_error_entry,
                                                                                ):
        with self.app.app_context():
            APIException('message', 'content', error_type="type", status_code=500, is_error=True)

        mock_error_entry.assert_called_once_with('type message : content')
        assert not mock_get_turnaround_in_ms.called

    @mock.patch.object(LoggerAPI, 'error_entry', return_value=None)
    @mock.patch('src.responses.get_turnaround_in_ms', return_value=50)
    def test_should_return_APIException_error_response_with_request_and_request_start_time_on_error(self,
                                                                                                    mock_get_turnaround_in_ms,
                                                                                                    mock_error_entry,
                                                                                                    ):
        with self.app.app_context():
            g.request_id = "request_id"
            g.start_time = 150.0
            APIException('message', 'content', error_type="type", status_code=500, is_error=True)

        mock_error_entry.assert_called_once_with('request_id - 50.0000 - 500 type message : content')
        mock_get_turnaround_in_ms.assert_called_once_with(150.0)

    @mock.patch.object(LoggerAPI, 'warning_entry', return_value=None)
    @mock.patch('src.responses.get_turnaround_in_ms', return_value=50)
    def test_should_return_APIException_error_response_with_request_and_request_start_time_on_warning(self,
                                                                                                      mock_get_turnaround_in_ms,
                                                                                                      mock_warn_entry,
                                                                                                      ):
        with self.app.app_context():
            g.request_id = "request_id"
            g.start_time = 150.0
            APIException('message', 'content', error_type="type", status_code=500, is_error=False)

        mock_warn_entry.assert_called_once_with('request_id - 50.0000 - 500 type message : content')
        mock_get_turnaround_in_ms.assert_called_once_with(150.0)

    def test_should_return_APIException_response(self):
        with mock.patch.object(APIException, '__init__', return_value=None):
            exception = APIException('', '', error_type="type", status_code=500, is_error=False)
            exception.error_type = "type"
            exception.status_code = 500
            exception.msg = "message"

        with self.app.app_context():
            actual = exception.get_response_json()

        self.assertEqual(actual.status_code, 500)
        self.assertEqual(actual.data, b'{"error":{"message":"message","type":"type"}}\n')
        self.assertEqual(actual.headers['Content-Type'], "application/json")

    @mock.patch.object(APIException, '__init__', return_value=None)
    def test_should_return_auth_exception(self,
                                          mock_api):
        with self.app.app_context():
            SecurityException('message', 'content')

        mock_api.assert_called_once_with(
            'message',
            'content',
            error_type='SecurityException',
            status_code=401,
            is_error=False
        )

    @mock.patch.object(APIException, '__init__', return_value=None)
    def test_should_return_runtime_exception(self,
                                             mock_api):
        with self.app.app_context():
            RuntimeException('message', 'content')

        mock_api.assert_called_once_with(
            'message',
            'content',
            error_type='RuntimeException',
            status_code=500
        )

    @mock.patch.object(APIException, '__init__', return_value=None)
    def test_should_return_validation_exception(self,
                                                mock_api):
        with self.app.app_context():
            DataValidationException('message', 'content')

        mock_api.assert_called_once_with(
            'message',
            'content',
            error_type='DataValidationException',
            status_code=400,
            is_error=False
        )

    @mock.patch.object(APIException, '__init__', return_value=None)
    def test_should_return_table_not_found_exception(self,
                                                     mock_api):
        with self.app.app_context():
            TableNotFoundException('table_name')

        mock_api.assert_called_once_with(
            '', 'table_name', error_type='TableNotFoundException', status_code=2
        )

    @mock.patch.object(APIException, '__init__', return_value=None)
    def test_should_return_db_connection_exception(self,
                                                   mock_api):
        with self.app.app_context():
            DBConnectionException('message')

        mock_api.assert_called_once_with(
            '',
            'message',
            error_type='DBConnectionException',
            status_code=0
        )

    @mock.patch.object(APIException, '__init__', return_value=None)
    def test_should_return_db_execution_exception(self,
                                                  mock_api):
        with self.app.app_context():
            DBExecutionException('operation', 'message')

        mock_api.assert_called_once_with(
            'operation',
            'message',
            error_type='DBExecutionException',
            status_code=1
        )

    @mock.patch.object(APIException, '__init__', return_value=None)
    def test_should_return_the_record_not_found_exception(self,
                                                          mock_api):
        with self.app.app_context():
            RecordNotFoundException('table', 'r_id')

        mock_api.assert_called_once_with('r_id', 'table', error_type='RecordNotFoundException', status_code=404)

    @mock.patch("time.perf_counter", return_value=200.0)
    def test_should_return_500000_when_current_200_and_req_time_150_on_turnaround_in_ms(self, mock_perf):
        request_start_time = 150.0

        result = get_turnaround_in_ms(request_start_time)

        expected = (200.0 - 150.0) * 1e4

        mock_perf.assert_called_once()
        self.assertEqual(result, expected)
