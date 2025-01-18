import unittest
from unittest import mock

from src.app import App
from src.caching import Caching
from src.config import Config
from src.responses import ValidResponse, APIException, APIResponse, CachedResponse
from src.user.service import UserServices


class UserControllerTest(unittest.TestCase):

    @mock.patch.object(APIResponse, 'get_response_json', return_value='response_json')
    @mock.patch.object(ValidResponse, '__init__', return_value=None)
    @mock.patch.object(ValidResponse, 'get_data', return_value={})
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_user_data', return_value={})
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch('flask_caching.Cache.get')
    @mock.patch('flask_caching.Cache.set')
    def test_should_return_valid_user_data_and_cache_response(self,
                                                              mock_cache_set,
                                                              mock_cache_get,
                                                              mock_secret_config,
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

        mock_cache_get.assert_called_once_with('myapp:app_user/')
        mock_cache_set.assert_called_once_with('myapp:app_user/', {}, timeout=60)
        mock_service.assert_called_once_with()
        mock_user_data.assert_called_once_with("")
        mock_response_get_data.assert_called_once_with()
        mock_response_init.assert_called_once_with(domain='Retrieved user data', detail='', data={})
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(APIResponse, 'get_response_json', return_value='response_json')
    @mock.patch.object(CachedResponse, '__init__', return_value=None)
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_user_data', return_value={})
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch('flask_caching.Cache.get')
    @mock.patch('flask_caching.Cache.set')
    def test_should_return_cached_user_data_response(self,
                                                     mock_cache_set,
                                                     mock_cache_get,
                                                     mock_secret_config,
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
                    headers={'x-api-key': 'test_key'},
                )

        mock_cache_get.assert_called_once_with('myapp:app_user/')
        assert not mock_cache_set.called
        assert not mock_service.called
        assert not mock_user_data.called
        mock_response_init.assert_called_once_with(key='myapp:app_user/', data={})
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(APIException, 'get_response_json', return_value='response_json')
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_user_data')
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch('flask_caching.Cache.get')
    @mock.patch('flask_caching.Cache.set')
    def test_should_return_error_response_on_get_user(self,
                                                      mock_cache_set,
                                                      mock_cache_get,
                                                      mock_secret_config,
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
                    headers={'x-api-key': 'test_key'},
                )

        mock_cache_get.assert_called_once_with('myapp:app_user/')
        assert not mock_cache_set.called
        mock_service.assert_called_once_with()
        mock_user_data.assert_called_once_with("")
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)
