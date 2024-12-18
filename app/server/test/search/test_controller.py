import unittest
from unittest import mock

from src.app import APP
from src.config import Config
from src.responses import ValidResponse, APIException
from src.search.service import SearchServices


class SearchControllerTest(unittest.TestCase):

    @mock.patch.object(ValidResponse, 'get_response_json', return_value=[])
    @mock.patch.object(ValidResponse, '__init__', return_value=None)
    @mock.patch.object(SearchServices, '__init__', return_value=None)
    @mock.patch.object(SearchServices, 'search', return_value=[])
    @mock.patch.object(Config, 'get_api_keys')
    def test_should_return_list_of_result_response_on_search_by_text(self,
                                                                     mock_secret_config,
                                                                     mock_search,
                                                                     mock_service_init,
                                                                     mock_response_init,
                                                                     mock_response
                                                                     ):
        mock_secret_config.return_value = ['test_key']
        expected_response_data = b'[]\n'
        with APP.test_client() as c:
            actual_response = c.get("/api/search/text",
                                    headers={
                                        'x-api-key': 'test_key',
                                    },
                                    )

            mock_search.assert_called_once_with("text")
            mock_service_init.assert_called_once_with()
            mock_response_init.assert_called_once_with(domain='Search Results', detail='text', content=[])
            mock_response.assert_called_once_with()
            self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(APIException, 'get_response_json', return_value='response_json')
    @mock.patch.object(APIException, '__init__', return_value=None)
    @mock.patch.object(SearchServices, '__init__', return_value=None)
    @mock.patch.object(SearchServices, 'search')
    @mock.patch.object(Config, 'get_api_keys')
    def test_should_return_api_error_response_on_search_by_text(self,
                                                                mock_secret_config,
                                                                mock_search,
                                                                mock_service_init,
                                                                mock_response_init,
                                                                mock_response
                                                                ):
        mock_secret_config.return_value = ['test_key']
        mock_search.side_effect = APIException(
            "msg",
            "content",
            "error_type",
            500
        )
        expected_response_data = b'response_json'
        with APP.test_client() as c:
            actual_response = c.get("/api/search/text",
                                    headers={
                                        'x-api-key': 'test_key',
                                    },
                                    )

            mock_service_init.assert_called_once_with()
            mock_search.assert_called_once_with("text")
            mock_response.assert_called_once_with()
            self.assertEqual(expected_response_data, actual_response.data)
