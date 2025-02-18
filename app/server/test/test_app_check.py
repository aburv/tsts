import unittest
from unittest import mock

from src.app import App
from src.caching import Caching
from src.config import Config
from src.responses import SecurityException, APIException


class PingControllerTest(unittest.TestCase):

    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Caching, 'init_cache')
    def test_should_return_success_response_on_ping_call(self, mock_init_caching, mock_keys):
        mock_keys.return_value = ['test_key']

        expected_response_data = b'{"data":"success"}\n'

        app = App.create()
        with app.test_client() as c:
            actual_response = c.post("/api/ping/",
                                     headers={'x-api-key': 'test_key'})

        mock_keys.assert_called_once_with()

        mock_init_caching.assert_called_once_with(app)

        self.assertEqual(expected_response_data, actual_response.data)
        self.assertEqual(200, actual_response.status_code)

    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(SecurityException, 'get_response_json')
    @mock.patch.object(APIException, '__init__', return_value=None)
    def test_should_return_authentication_exception_response_on_ping_call(self,
                                                                          mock_exception_init,
                                                                          mock_response,
                                                                          mock_keys):
        mock_keys.return_value = ['test_key']
        mock_exception_init.status_code = 401
        response = b'{"error":' \
                   b'{"detail":"Not Authenticated",' \
                   b'"message":"Client"' \
                   b'"type":"AuthenticationException"}}\n'
        mock_response.return_value = response
        expected_response_data = response

        with mock.patch.object(Caching, 'init_cache'):
            app = App.create()
            with app.test_client() as c:
                actual_response = c.post("/api/ping/",
                                         headers={'x-api-key': 'invalid_key'})

        mock_keys.assert_called()
        mock_exception_init.assert_called_once_with('Client', 'Not Authenticated',
                                                    error_type='SecurityException',
                                                    status_code=401)
        self.assertEqual(expected_response_data, actual_response.data)

    def test_should_return_success_response_on_aws_ping(self):
        expected_response_data = b'{"data":"success"}\n'

        with mock.patch.object(Caching, 'init_cache'):
            app = App.create()
            with app.test_client() as c:
                actual_response = c.get("/api/ping/aws")

        self.assertEqual(expected_response_data, actual_response.data)
        self.assertEqual(200, actual_response.status_code)
