import unittest
from unittest import mock

from src.app import App
from src.caching import Caching
from src.config import Config
from src.responses import ValidResponse, APIException, APIResponse, CachedResponse
from src.search.service import SearchServices


class SearchControllerTest(unittest.TestCase):

    @mock.patch.object(APIResponse, 'get_response_json', return_value=[])
    @mock.patch.object(ValidResponse, '__init__', return_value=None)
    @mock.patch.object(ValidResponse, 'get_data', return_value=[])
    @mock.patch.object(SearchServices, '__init__', return_value=None)
    @mock.patch.object(SearchServices, 'search', return_value=[])
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch('flask_caching.Cache.get')
    @mock.patch('flask_caching.Cache.set')
    def test_should_return_list_of_result_response_and_cache_on_search_by_text(self,
                                                                               mock_cache_set,
                                                                               mock_cache_get,
                                                                               mock_secret_config,
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
                                        },
                                        )

        mock_cache_get.assert_called_once_with('myapp:search/text:text')
        mock_cache_set.assert_called_once_with('myapp:search/text:text', [], timeout=60)
        mock_search.assert_called_once_with("text")
        mock_service_init.assert_called_once_with()
        mock_response_init.assert_called_once_with(domain='Search Results', detail='text', data=[])
        mock_response_get_data.assert_called_once_with()
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(APIResponse, 'get_response_json', return_value=[])
    @mock.patch.object(CachedResponse, '__init__', return_value=None)
    @mock.patch.object(SearchServices, '__init__', return_value=None)
    @mock.patch.object(SearchServices, 'search')
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch('flask_caching.Cache.get')
    @mock.patch('flask_caching.Cache.set')
    def test_should_return_list_of_result_response_from_cache_on_search_by_text(self,
                                                                                mock_cache_set,
                                                                                mock_cache_get,
                                                                                mock_secret_config,
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
                                        },
                                        )

        mock_cache_get.assert_called_once_with('myapp:search/text:text')
        assert not mock_cache_set.called
        assert not mock_search.called
        assert not mock_service_init.called
        mock_response_init.assert_called_once_with(key='myapp:search/text:text', data=[])
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(APIException, 'get_response_json', return_value='response_json')
    @mock.patch.object(SearchServices, '__init__', return_value=None)
    @mock.patch.object(SearchServices, 'search')
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch('flask_caching.Cache.get')
    def test_should_return_api_error_response_on_search_by_text(self,
                                                                mock_cache_get,
                                                                mock_secret_config,
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
                                        },
                                        )

        mock_cache_get.assert_called_once_with('myapp:search/text:text')
        mock_service_init.assert_called_once_with()
        mock_search.assert_called_once_with("text")
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)
