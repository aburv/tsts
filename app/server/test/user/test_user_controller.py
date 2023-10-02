import unittest
from unittest import mock

from src.app import APP
from src.config import Config
from src.responses import ValidResponse, APIException


class UserControllerTest(unittest.TestCase):

    @mock.patch.object(ValidResponse, 'get_response_json', return_value='response_json')
    @mock.patch.object(ValidResponse, '__init__', return_value=None)
    @mock.patch.object(Config, 'get_api_key')
    def test_should_return_valid_instances_response(self,
                                                    mock_secret_config,
                                                    mock_response_init,
                                                    mock_response
                                                    ):
        mock_secret_config.return_value = 'test_key'
        expected_response_data = b'response_json'
        with APP.test_client() as c:
            actual_response = c.get("/api/user/app",
                                    headers={'x-api-key': 'test_key'},
                                    )

            mock_response_init.assert_called_once_with('retrieved user data',  {'data': 'success'})
            self.assertEqual(expected_response_data, actual_response.data)
