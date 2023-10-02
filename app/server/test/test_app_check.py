import unittest
from unittest import mock

from src.app import APP
from src.config import Config
from src.responses import SecurityException, APIException


class PingControllerTest(unittest.TestCase):

    @mock.patch.object(Config, 'get_api_key')
    def test_should_return_ping_response(self,
                                         mock_secret_config):
        mock_secret_config.return_value = 'test_key'

        expected_response_data = b'{"data":"success"}\n'

        with APP.test_client() as c:
            actual_response = c.post("/api/ping/",
                                     headers={'x-api-key': 'test_key'},
                                     content_type="application/json")

            self.assertEqual(expected_response_data, actual_response.data)
            self.assertEqual(200, actual_response.status_code)

    @mock.patch.object(Config, 'get_api_key')
    @mock.patch.object(SecurityException, 'get_response_json')
    @mock.patch.object(APIException, '__init__', return_value=None)
    def test_should_return_authentication_exception_response(self,
                                                             mock_exception_init,
                                                             mock_response,
                                                             mock_secret_config):
        mock_secret_config.return_value = 'test_key'
        mock_exception_init.status_code = 401
        response = b'{"error":' \
                   b'{"detail":"Not Authenticated",' \
                   b'"message":"Client"' \
                   b'"type":"AuthenticationException"}}\n'
        mock_response.return_value = response
        expected_response_data = response

        with APP.test_client() as c:
            actual_response = c.post("/api/ping/",
                                     headers={'x-api-key': 'invalid_key'},
                                     content_type="application/json")

            mock_secret_config.assert_called()
            mock_exception_init.assert_called_once_with('Client', 'Not Authenticated',
                                                        error_type='SecurityException',
                                                        status_code=401)
            self.assertEqual(expected_response_data, actual_response.data)

    def test_should_return_aws_ping_response(self):
        expected_response_data = b'{"data":"success"}\n'

        with APP.test_client() as c:
            actual_response = c.get("/api/ping/aws",
                                    content_type="application/json")

            self.assertEqual(expected_response_data, actual_response.data)
            self.assertEqual(200, actual_response.status_code)
