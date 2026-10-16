import unittest
from unittest import mock

from src.client.service import ClientSessionService
from src.responses import SecurityException, APIException
from test.test_app_config import get_app


class PingControllerTest(unittest.TestCase):

    @mock.patch.object(ClientSessionService, 'authenticate_request')
    def test_should_return_success_response_on_ping_call(self, mock_authenticate_request):
        mock_authenticate_request.return_value = True

        expected_response_data = b'{"data":"success"}\n'

        app = get_app()
        with app.test_client() as c:
            actual_response = c.post(
                "/api/ping/",
                headers={
                    'x-api-key': 'Client test_key',
                    'X-Client-Installation': 'installation_key',
                    'X-Client-Platform': 'web',
                    'X-Client-Timestamp': 'timestamp',
                    'X-Client-Request-Id': 'request_id',
                    'X-Client-Signature': 'signature'
                })

        mock_authenticate_request.assert_called_once_with('test_key', 'installation_key', 'web', 'timestamp',
                                                          'request_id', 'signature', 'POST', '/api/ping/', b'')

        self.assertEqual(expected_response_data, actual_response.data)
        self.assertEqual(200, actual_response.status_code)

    @mock.patch.object(ClientSessionService, 'authenticate_request')
    @mock.patch.object(SecurityException, 'get_response_json')
    @mock.patch.object(APIException, '__init__', return_value=None)
    def test_should_return_authentication_exception_response_when_client_key_is_invalid_on_ping_call(self,
                                                                                                     mock_exception_init,
                                                                                                     mock_response,
                                                                                                     mock_authenticate_request):
        mock_authenticate_request.return_value = False
        mock_exception_init.status_code = 401
        response = b'{"error":' \
                   b'{"detail":"Not Authenticated",' \
                   b'"message":"Client"' \
                   b'"type":"AuthenticationException"}}\n'
        mock_response.return_value = response
        expected_response_data = response

        app = get_app()
        with app.test_client() as c:
            actual_response = c.post(
                "/api/ping/",
                headers={
                    'x-api-key': 'Client test_key',
                    'X-Client-Installation': 'installation_key',
                    'X-Client-Platform': 'web',
                    'X-Client-Timestamp': 'timestamp',
                    'X-Client-Request-Id': 'request_id',
                    'X-Client-Signature': 'signature'
                })

        mock_authenticate_request.assert_called_once_with('test_key', 'installation_key', 'web', 'timestamp',
                                                          'request_id', 'signature', 'POST', '/api/ping/', b'')
        mock_exception_init.assert_called_once_with('Client', 'Not Authenticated',
                                                    error_type='SecurityException',
                                                    status_code=401, is_error=False)
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(ClientSessionService, 'authenticate_request')
    @mock.patch.object(SecurityException, 'get_response_json')
    @mock.patch.object(APIException, '__init__', return_value=None)
    def test_should_return_authentication_exception_response_when_client_key_is_empty_on_ping_call(self,
                                                                                                   mock_exception_init,
                                                                                                   mock_response,
                                                                                                   mock_authenticate_request):
        mock_exception_init.status_code = 401
        response = b'{"error":' \
                   b'{"detail":"Not Authenticated",' \
                   b'"message":"Client"' \
                   b'"type":"AuthenticationException"}}\n'
        mock_response.return_value = response
        expected_response_data = response

        app = get_app()
        with app.test_client() as c:
            actual_response = c.post("/api/ping/",
                                     headers={'x-api-key': ''})

        mock_authenticate_request.assert_not_called()
        mock_exception_init.assert_called_once_with('Client', 'Not Authenticated',
                                                    error_type='SecurityException',
                                                    status_code=401, is_error=False)
        self.assertEqual(expected_response_data, actual_response.data)

    def test_should_return_success_response_on_aws_ping(self):
        expected_response_data = b'{"data":"success"}\n'

        app = get_app()
        with app.test_client() as c:
            actual_response = c.get("/api/ping/aws")

        self.assertEqual(expected_response_data, actual_response.data)
        self.assertEqual(200, actual_response.status_code)
