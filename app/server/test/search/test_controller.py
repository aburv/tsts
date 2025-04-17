import unittest
from unittest import mock

from src.app import App
from src.caching import Caching
from src.config import Config
from src.responses import ValidResponse, APIException, APIResponse, CachedResponse
from src.search.service import SearchServices
from src.services.auth_service import AuthServices


class SearchControllerTest(unittest.TestCase):

    @mock.patch.object(APIResponse, 'get_response_json', return_value=[])
    @mock.patch.object(ValidResponse, '__init__', return_value=None)
    @mock.patch.object(ValidResponse, 'get_data', return_value=[])
    @mock.patch.object(SearchServices, '__init__', return_value=None)
    @mock.patch.object(SearchServices, 'search', return_value=[])
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    @mock.patch('flask_caching.Cache.get')
    @mock.patch('flask_caching.Cache.set')
    def test_should_return_list_of_result_response_and_cache_on_search_by_text(self,
                                                                               mock_cache_set,
                                                                               mock_cache_get,
                                                                               mock_get_tokens,
                                                                               mock_secret_config,
                                                                               mock_validate_token,
                                                                               mock_auth_service,
                                                                               mock_search,
                                                                               mock_service_init,
                                                                               mock_response_get_data,
                                                                               mock_response_init,
                                                                               mock_response
                                                                               ):
        mock_cache_get.return_value = None

        mock_secret_config.return_value = ['test_key']
        expected_response_data = b'[]\n'

        with mock.patch.object(Caching, 'init_cache'):
            app = App.create()
            with app.test_client() as c:
                actual_response = c.get("/api/search/text",
                                        headers={
                                            'x-api-key': 'test_key',
                                            'x-access-key': 'token',
                                        },
                                        )

        mock_cache_get.assert_called_once_with('myapp:search/text:text/user_id:user_id')
        mock_cache_set.assert_called_once_with('myapp:search/text:text/user_id:user_id', [], timeout=60)
        mock_search.assert_called_once_with('text', 'user_id')
        mock_service_init.assert_called_once_with()
        mock_secret_config.assert_called_once_with()
        mock_get_tokens.assert_called_once_with('token')
        mock_auth_service.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', '', '', '')
        mock_response_init.assert_called_once_with(domain='Search Results', detail='text', data=[])
        mock_response_get_data.assert_called_once_with()
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(APIResponse, 'get_response_json', return_value=[])
    @mock.patch.object(CachedResponse, '__init__', return_value=None)
    @mock.patch.object(SearchServices, '__init__', return_value=None)
    @mock.patch.object(SearchServices, 'search')
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    @mock.patch('flask_caching.Cache.get')
    @mock.patch('flask_caching.Cache.set')
    def test_should_return_list_of_result_response_from_cache_on_search_by_text(self,
                                                                                mock_cache_set,
                                                                                mock_cache_get,
                                                                                mock_get_tokens,
                                                                                mock_secret_config,
                                                                                mock_validate_token,
                                                                                mock_auth_service,
                                                                                mock_search,
                                                                                mock_service_init,
                                                                                mock_response_init,
                                                                                mock_response
                                                                                ):
        mock_cache_get.return_value = []

        mock_secret_config.return_value = ['test_key']
        expected_response_data = b'[]\n'

        with mock.patch.object(Caching, 'init_cache'):
            app = App.create()
            with app.test_client() as c:
                actual_response = c.get("/api/search/text",
                                        headers={
                                            'x-api-key': 'test_key',
                                            'x-access-key': 'token',
                                        },
                                        )

        mock_cache_get.assert_called_once_with('myapp:search/text:text/user_id:user_id')
        assert not mock_cache_set.called
        mock_secret_config.assert_called_once_with()
        mock_get_tokens.assert_called_once_with('token')
        mock_auth_service.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', '', '', '')
        assert not mock_search.called
        assert not mock_service_init.called
        mock_response_init.assert_called_once_with(key='myapp:search/text:text/user_id:user_id', data=[])
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(APIException, 'get_response_json', return_value='response_json')
    @mock.patch.object(SearchServices, '__init__', return_value=None)
    @mock.patch.object(SearchServices, 'search')
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    @mock.patch('flask_caching.Cache.get')
    def test_should_return_api_error_response_on_search_by_text(self,
                                                                mock_cache_get,
                                                                mock_get_tokens,
                                                                mock_secret_config,
                                                                mock_validate_token,
                                                                mock_auth_service,
                                                                mock_search,
                                                                mock_service_init,
                                                                mock_response
                                                                ):
        mock_cache_get.return_value = None
        mock_secret_config.return_value = ['test_key']
        with mock.patch.object(APIException, "__init__", return_value=None):
            mock_search.side_effect = APIException(
                "msg",
                "content",
                "error_type",
                500
            )
        expected_response_data = b'response_json'

        with mock.patch.object(Caching, 'init_cache'):
            app = App.create()
            with app.test_client() as c:
                actual_response = c.get("/api/search/text",
                                        headers={
                                            'x-api-key': 'test_key',
                                            'x-access-key': 'token'
                                        },
                                        )

        mock_cache_get.assert_called_once_with('myapp:search/text:text/user_id:user_id')
        mock_secret_config.assert_called_once_with()
        mock_get_tokens.assert_called_once_with('token')
        mock_auth_service.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', '', '', '')
        mock_service_init.assert_called_once_with()
        mock_search.assert_called_once_with('text', 'user_id')
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(APIResponse, 'get_response_json', return_value='response_json')
    @mock.patch.object(ValidResponse, '__init__', return_value=None)
    @mock.patch.object(ValidResponse, 'get_data', return_value={})
    @mock.patch.object(SearchServices, '__init__', return_value=None)
    @mock.patch.object(SearchServices, 'search', return_value=[])
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    @mock.patch('flask_caching.Cache.get')
    @mock.patch('flask_caching.Cache.set')
    def test_should_return_valid_search_results_and_cache_response_when_no_access_token(self,
                                                                                        mock_cache_set,
                                                                                        mock_cache_get,
                                                                                        mock_get_tokens,
                                                                                        mock_secret_config,
                                                                                        mock_validate_token,
                                                                                        mock_auth_service,
                                                                                        mock_search_results,
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
                    "/api/search/tt",
                    headers={'x-api-key': 'test_key'},
                )

        mock_cache_get.assert_called_once_with('myapp:search/text:tt/user_id:None')
        mock_cache_set.assert_called_once_with('myapp:search/text:tt/user_id:None', {}, timeout=60)
        mock_secret_config.assert_called_once_with()
        assert not mock_get_tokens.called
        assert not mock_auth_service.called
        assert not mock_validate_token.called
        mock_service.assert_called_once_with()
        mock_search_results.assert_called_once_with('tt', None)
        mock_response_get_data.assert_called_once_with()
        mock_response_init.assert_called_once_with(domain='Search Results', detail='tt', data=[])
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)
