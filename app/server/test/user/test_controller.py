import unittest
from unittest import mock

from src.app import App
from src.caching import Caching
from src.config import Config
from src.responses import ValidResponse, APIException, APIResponse, CachedResponse
from src.services.auth_service import AuthServices
from src.user.service import UserServices


class UserControllerTest(unittest.TestCase):

    @mock.patch.object(APIResponse, 'get_response_json', return_value='response_json')
    @mock.patch.object(ValidResponse, '__init__', return_value=None)
    @mock.patch.object(ValidResponse, 'get_data', return_value={})
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_user_data', return_value={})
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    @mock.patch('flask_caching.Cache.get')
    @mock.patch('flask_caching.Cache.set')
    def test_should_return_valid_user_data_and_cache_response(self,
                                                              mock_cache_set,
                                                              mock_cache_get,
                                                              mock_get_tokens,
                                                              mock_secret_config,
                                                              mock_validate_token,
                                                              mock_auth_service,
                                                              mock_user_data,
                                                              mock_service,
                                                              mock_response_get_data,
                                                              mock_response_init,
                                                              mock_response
                                                              ):
        mock_cache_get.return_value = None

        mock_secret_config.return_value = 'test_key'
        expected_response_data = b'response_json'

        with mock.patch.object(Caching, 'init_cache'):
            app = App.create()
            with app.test_client() as c:
                actual_response = c.get(
                    "/api/user/app",
                    headers={'x-api-key': 'test_key', 'x-access-key': 'token'},
                )

        mock_cache_get.assert_called_once_with('myapp:app_user/user_id:user_id')
        mock_cache_set.assert_called_once_with('myapp:app_user/user_id:user_id', {}, timeout=60)
        mock_secret_config.assert_called_once_with()
        mock_get_tokens.assert_called_once_with('token')
        mock_auth_service.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', '', '', '')
        mock_service.assert_called_once_with()
        mock_user_data.assert_called_once_with('user_id')
        mock_response_get_data.assert_called_once_with()
        mock_response_init.assert_called_once_with(domain='Retrieved user data', detail='user_id', data={})
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(APIResponse, 'get_response_json', return_value='response_json')
    @mock.patch.object(ValidResponse, '__init__', return_value=None)
    @mock.patch.object(ValidResponse, 'get_data', return_value={})
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_user_data', return_value={})
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    @mock.patch('flask_caching.Cache.get')
    @mock.patch('flask_caching.Cache.set')
    def test_should_return_valid_user_data_and_cache_response_when_no_access_token(self,
                                                                                   mock_cache_set,
                                                                                   mock_cache_get,
                                                                                   mock_get_tokens,
                                                                                   mock_secret_config,
                                                                                   mock_validate_token,
                                                                                   mock_auth_service,
                                                                                   mock_user_data,
                                                                                   mock_service,
                                                                                   mock_response_get_data,
                                                                                   mock_response_init,
                                                                                   mock_response
                                                                                   ):
        mock_cache_get.return_value = None

        mock_secret_config.return_value = 'test_key'
        expected_response_data = b'response_json'

        with mock.patch.object(Caching, 'init_cache'):
            app = App.create()
            with app.test_client() as c:
                actual_response = c.get(
                    "/api/user/app",
                    headers={'x-api-key': 'test_key'},
                )

        mock_cache_get.assert_called_once_with('myapp:app_user/user_id:None')
        mock_cache_set.assert_called_once_with('myapp:app_user/user_id:None', {}, timeout=60)
        mock_secret_config.assert_called_once_with()
        assert not mock_get_tokens.called
        assert not mock_auth_service.called
        assert not mock_validate_token.called
        mock_service.assert_called_once_with()
        mock_user_data.assert_called_once_with(None)
        mock_response_get_data.assert_called_once_with()
        mock_response_init.assert_called_once_with(domain='Retrieved user data', detail=None, data={})
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(APIResponse, 'get_response_json', return_value='response_json')
    @mock.patch.object(CachedResponse, '__init__', return_value=None)
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_user_data', return_value={})
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    @mock.patch('flask_caching.Cache.get')
    @mock.patch('flask_caching.Cache.set')
    def test_should_return_cached_user_data_response(self,
                                                     mock_cache_set,
                                                     mock_cache_get,
                                                     mock_get_tokens,
                                                     mock_secret_config,
                                                     mock_validate_token,
                                                     mock_auth_service,
                                                     mock_user_data,
                                                     mock_service,
                                                     mock_response_init,
                                                     mock_response
                                                     ):
        mock_cache_get.return_value = {}

        mock_secret_config.return_value = 'test_key'
        expected_response_data = b'response_json'

        with mock.patch.object(Caching, 'init_cache'):
            app = App.create()
            with app.test_client() as c:
                actual_response = c.get(
                    "/api/user/app",
                    headers={'x-api-key': 'test_key', 'x-access-key': 'token'},
                )

        mock_cache_get.assert_called_once_with('myapp:app_user/user_id:user_id')
        assert not mock_cache_set.called
        assert not mock_service.called
        assert not mock_user_data.called
        mock_secret_config.assert_called_once_with()
        mock_get_tokens.assert_called_once_with('token')
        mock_auth_service.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', '', '', '')
        mock_response_init.assert_called_once_with(key='myapp:app_user/user_id:user_id', data={})
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(APIException, 'get_response_json', return_value='response_json')
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_user_data')
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    @mock.patch('flask_caching.Cache.get')
    @mock.patch('flask_caching.Cache.set')
    def test_should_return_error_response_on_get_user(self,
                                                      mock_cache_set,
                                                      mock_cache_get,
                                                      mock_get_tokens,
                                                      mock_secret_config,
                                                      mock_validate_token,
                                                      mock_auth_service,
                                                      mock_user_data,
                                                      mock_service,
                                                      mock_response
                                                      ):
        mock_cache_get.return_value = None

        mock_secret_config.return_value = 'test_key'

        with mock.patch.object(APIException, '__init__', return_value=None):
            mock_user_data.side_effect = APIException(
                "msg",
                "content",
                "error_type",
                500
            )
        expected_response_data = b'response_json'

        with mock.patch.object(Caching, 'init_cache'):
            app = App.create()
            with app.test_client() as c:
                actual_response = c.get(
                    "/api/user/app",
                    headers={'x-api-key': 'test_key', 'x-access-key': 'token'},
                )

        mock_cache_get.assert_called_once_with('myapp:app_user/user_id:user_id')
        assert not mock_cache_set.called
        mock_secret_config.assert_called_once_with()
        mock_get_tokens.assert_called_once_with('token')
        mock_auth_service.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', '', '', '')
        mock_service.assert_called_once_with()
        mock_user_data.assert_called_once_with('user_id')
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(APIResponse, 'get_response_json', return_value='response_json')
    @mock.patch.object(ValidResponse, '__init__', return_value=None)
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'done_user_onboarding', return_value='t')
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    def test_should_return_t_valid_response_on_set_done_onboarding(self,
                                                                   mock_get_tokens,
                                                                   mock_secret_config,
                                                                   mock_validate_token,
                                                                   mock_auth_service,
                                                                   mock_done_user_onboarding,
                                                                   mock_service,
                                                                   mock_response_init,
                                                                   mock_response
                                                                   ):
        mock_secret_config.return_value = 'test_key'
        expected_response_data = b'response_json'

        with mock.patch.object(Caching, 'init_cache'):
            app = App.create()
            with app.test_client() as c:
                actual_response = c.post(
                    "/api/user/done_onboarding",
                    json={'data': {}},
                    headers={'x-api-key': 'test_key', 'x-access-key': 'token'},
                )

        mock_secret_config.assert_called_once_with()
        mock_get_tokens.assert_called_once_with('token')
        mock_auth_service.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', '', '', '')
        mock_service.assert_called_once_with()
        mock_done_user_onboarding.assert_called_once_with('user_id')
        mock_response_init.assert_called_once_with(domain='Done user onboarding', detail='user_id', data='t')
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)
