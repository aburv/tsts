import unittest
from unittest import mock

from src.app import APP
from src.config import Config
from src.responses import ValidResponse, APIException
from src.user.service import UserServices


class UserControllerTest(unittest.TestCase):

    @mock.patch.object(ValidResponse, 'get_response_json', return_value='response_json')
    @mock.patch.object(ValidResponse, '__init__', return_value=None)
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_user_data', return_value={})
    @mock.patch.object(Config, 'get_api_keys')
    def test_should_return_valid_user_data_response(self,
                                                    mock_secret_config,
                                                    mock_user_data,
                                                    mock_service,
                                                    mock_response_init,
                                                    mock_response
                                                    ):
        mock_secret_config.return_value = 'test_key'
        expected_response_data = b'response_json'
        with APP.test_client() as c:
            actual_response = c.get(
                "/api/user/app",
                headers={'x-api-key': 'test_key'},
            )

            mock_service.assert_called_once_with()
            mock_user_data.assert_called_once_with("")
            mock_response_init.assert_called_once_with(domain='Retrieved user data', detail='', content={})
            mock_response.assert_called_once_with()
            self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(APIException, 'get_response_json', return_value='response_json')
    @mock.patch.object(APIException, '__init__', return_value=None)
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_user_data')
    @mock.patch.object(Config, 'get_api_keys')
    def test_should_return_error_response_on_get_user(self,
                                                      mock_secret_config,
                                                      mock_user_data,
                                                      mock_service,
                                                      mock_response_init,
                                                      mock_response
                                                      ):
        mock_secret_config.return_value = 'test_key'
        mock_user_data.side_effect = APIException(
            "msg",
            "content",
            "error_type",
            500
        )
        expected_response_data = b'response_json'
        with APP.test_client() as c:
            actual_response = c.get(
                "/api/user/app",
                headers={'x-api-key': 'test_key'},
            )

            mock_service.assert_called_once_with()
            mock_user_data.assert_called_once_with("")
            mock_response.assert_called_once_with()
            self.assertEqual(expected_response_data, actual_response.data)
