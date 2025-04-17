import unittest
from unittest import mock

from src.app import App
from src.caching import Caching
from src.config import Config
from src.login.service import LoginServices
from src.responses import ValidResponse, APIException, DataValidationException


class LoginControllerTest(unittest.TestCase):

    @mock.patch.object(ValidResponse, 'get_response_json', return_value='response_json')
    @mock.patch.object(ValidResponse, '__init__', return_value=None)
    @mock.patch.object(LoginServices, '__init__', return_value=None)
    @mock.patch.object(LoginServices, 'login', return_value='auth_token')
    @mock.patch.object(Config, 'get_api_keys')
    def test_should_return_valid_auth_token_response_on_get_user_token(self,
                                                                       mock_secret_config,
                                                                       mock_login,
                                                                       mock_service_init,
                                                                       mock_response_init,
                                                                       mock_response
                                                                       ):
        mock_secret_config.return_value = ['test_key']
        expected_response_data = b'response_json'

        with mock.patch.object(Caching, 'init_cache'):
            app = App.create()
            with app.test_client() as c:
                actual_response = c.post("/api/auth/login",
                                         headers={
                                             'x-api-key': 'test_key',
                                             'content-type': 'application/json'
                                         },
                                         json={'data': {'user': {'user': 'test'}, 'login': {'login': 'login'}}}
                                         )

        mock_service_init.assert_called_once_with()
        mock_login.assert_called_once_with({'user': 'test'}, {'login': 'login', 'ip': '127.0.0.1'})
        mock_response_init.assert_called_once_with(domain='Get user token', data='auth_token',
                                                   detail="{'user': 'test'} {'login': 'login', 'ip': '127.0.0.1'}")
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(APIException, 'get_response_json', return_value='response_json')
    @mock.patch.object(LoginServices, '__init__', return_value=None)
    @mock.patch.object(LoginServices, 'login')
    @mock.patch.object(Config, 'get_api_keys')
    def test_should_return_api_error_response_on_get_user_token(self,
                                                                mock_secret_config,
                                                                mock_login,
                                                                mock_service_init,
                                                                mock_response
                                                                ):
        mock_secret_config.return_value = ['test_key']
        with mock.patch.object(APIException, '__init__', return_value=None):
            mock_login.side_effect = APIException(
                "msg",
                "content",
                "error_type",
                500
            )
        expected_response_data = b'response_json'

        with mock.patch.object(Caching, 'init_cache'):
            app = App.create()
            with app.test_client() as c:
                actual_response = c.post("/api/auth/login",
                                         headers={
                                             'x-api-key': 'test_key',
                                             'content-type': 'application/json'
                                         },
                                         json={
                                             'data': {
                                                 'user': {"user": "test"},
                                                 'login': {"login": "login"}
                                             }
                                         }
                                         )

        mock_service_init.assert_called_once_with()
        mock_login.assert_called_once_with({'user': 'test'}, {'login': 'login', 'ip': '127.0.0.1'})
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(APIException, 'get_response_json', return_value='response_json')
    @mock.patch.object(DataValidationException, '__init__', return_value=None)
    @mock.patch.object(LoginServices, '__init__', return_value=None)
    @mock.patch.object(LoginServices, 'login')
    @mock.patch.object(Config, 'get_api_keys')
    def test_should_raise_data_validation_return_error_response_when_no_data_on_get_user_token(
            self,
            mock_secret_config,
            mock_login,
            mock_service_init,
            mock_exception,
            mock_response
    ):
        mock_secret_config.return_value = ['test_key']
        expected_response_data = b'response_json'

        with mock.patch.object(Caching, 'init_cache'):
            app = App.create()
            with app.test_client() as c:
                actual_response = c.post("/api/auth/login",
                                         headers={
                                             'x-api-key': 'test_key',
                                             'content-type': 'application/json'
                                         },
                                         json={}
                                         )

        assert not mock_service_init.called
        assert not mock_login.called
        mock_exception.assert_called_once_with('Login', 'No Data')
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(APIException, 'get_response_json', return_value='response_json')
    @mock.patch.object(DataValidationException, '__init__', return_value=None)
    @mock.patch.object(LoginServices, '__init__', return_value=None)
    @mock.patch.object(LoginServices, 'login')
    @mock.patch.object(Config, 'get_api_keys')
    def test_should_raise_data_validation_return_error_response_when_no_user_data_on_get_user_token(
            self,
            mock_secret_config,
            mock_login,
            mock_service_init,
            mock_exception,
            mock_response
    ):
        mock_secret_config.return_value = ['test_key']
        expected_response_data = b'response_json'

        with mock.patch.object(Caching, 'init_cache'):
            app = App.create()
            with app.test_client() as c:
                actual_response = c.post("/api/auth/login",
                                         headers={
                                             'x-api-key': 'test_key',
                                             'content-type': 'application/json'
                                         },
                                         json={
                                             'data': {
                                                 'login': {"login": "login"}
                                             }
                                         }
                                         )

        assert not mock_service_init.called
        assert not mock_login.called
        mock_exception.assert_called_once_with("Login None {'login': 'login'}", 'No user Data')
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(APIException, 'get_response_json', return_value='response_json')
    @mock.patch.object(DataValidationException, '__init__', return_value=None)
    @mock.patch.object(LoginServices, '__init__', return_value=None)
    @mock.patch.object(LoginServices, 'login')
    @mock.patch.object(Config, 'get_api_keys')
    def test_should_raise_data_validation_return_error_response_when_no_login_data_on_get_user_token(
            self,
            mock_secret_config,
            mock_login,
            mock_service_init,
            mock_exception,
            mock_response
    ):
        mock_secret_config.return_value = ['test_key']
        expected_response_data = b'response_json'

        with mock.patch.object(Caching, 'init_cache'):
            app = App.create()
            with app.test_client() as c:
                actual_response = c.post("/api/auth/login",
                                         headers={
                                             'x-api-key': 'test_key',
                                             'content-type': 'application/json'
                                         },
                                         json={
                                             'data': {
                                                 'user': {"user": "test"},
                                             }
                                         }
                                         )

        assert not mock_service_init.called
        assert not mock_login.called
        mock_exception.assert_called_once_with("Login {'user': 'test'} None", 'No login Data')
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(ValidResponse, 'get_response_json', return_value='response_json')
    @mock.patch.object(ValidResponse, '__init__', return_value=None)
    @mock.patch.object(LoginServices, 'refresh', return_value='refresh_token')
    @mock.patch.object(Config, 'get_api_keys')
    def test_should_return_valid_token_response_on_refresh_user_access_token(self,
                                                                             mock_secret_config,
                                                                             mock_refresh,
                                                                             mock_response_init,
                                                                             mock_response
                                                                             ):
        mock_secret_config.return_value = ['test_key']
        expected_response_data = b'response_json'

        with mock.patch.object(Caching, 'init_cache'):
            app = App.create()
            with app.test_client() as c:
                actual_response = c.get("/api/auth/refresh_token",
                                        headers={
                                            'x-api-key': 'test_key',
                                            'x-access-key': 'token'
                                        }
                                        )

        mock_refresh.assert_called_once_with('token')
        mock_response_init.assert_called_once_with(domain='Get updated user access token',
                                                   data='refresh_token', detail='token')
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(APIException, 'get_response_json', return_value='response_json')
    @mock.patch.object(LoginServices, 'refresh')
    @mock.patch.object(Config, 'get_api_keys')
    def test_should_return_api_error_response_on_refresh_user_access_token(self,
                                                                           mock_secret_config,
                                                                           mock_refresh,
                                                                           mock_response
                                                                           ):
        mock_secret_config.return_value = ['test_key']

        with mock.patch.object(APIException, '__init__', return_value=None):
            mock_refresh.side_effect = APIException(
                "msg",
                "content",
                "error_type",
                500
            )
        expected_response_data = b'response_json'
        with mock.patch.object(Caching, 'init_cache'):
            app = App.create()
            with app.test_client() as c:
                actual_response = c.get("/api/auth/refresh_token",
                                        headers={
                                            'x-api-key': 'test_key',
                                            'x-access-key': 'token'
                                        }
                                        )

        mock_refresh.assert_called_once_with('token')
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)
