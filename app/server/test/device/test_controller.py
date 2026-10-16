import unittest
from unittest import mock

from src.client.service import ClientSessionService
from src.device.service import DeviceServices
from src.responses import ValidResponse, APIException, APIResponse
from test.test_app_config import get_app


class DeviceControllerTest(unittest.TestCase):

    @mock.patch.object(APIResponse, 'get_response_json', return_value='response_json')
    @mock.patch.object(ValidResponse, '__init__', return_value=None)
    @mock.patch.object(DeviceServices, '__init__', return_value=None)
    @mock.patch.object(DeviceServices, 'register_device', return_value='device_id')
    @mock.patch.object(ClientSessionService, 'authenticate_request')
    def test_should_return_valid_device_data_response_on_register_device(self,
                                                                         mock_authenticate_request,
                                                                         mock_register_device,
                                                                         mock_service_init,
                                                                         mock_response_init,
                                                                         mock_response
                                                                         ):
        mock_authenticate_request.return_value = True
        expected_response_data = b'response_json'

        app = get_app()
        with app.test_client() as c:
            actual_response = c.post("/api/device/register",
                                     headers={
                                         'x-api-key': 'Client test_key',
                                     },
                                     json={'data': {}}
                                     )

        mock_service_init.assert_called_once_with()
        mock_register_device.assert_called_once_with({})
        mock_response_init.assert_called_once_with(domain='New Device', detail={}, data='device_id')
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(APIException, 'get_response_json', return_value='response_json')
    @mock.patch.object(DeviceServices, '__init__', return_value=None)
    @mock.patch.object(DeviceServices, 'register_device')
    @mock.patch.object(ClientSessionService, 'authenticate_request')
    def test_should_return_api_error_response_on_register_device(self,
                                                                 mock_authenticate_request,
                                                                 mock_register_device,
                                                                 mock_service_init,
                                                                 mock_response
                                                                 ):
        mock_authenticate_request.return_value = True
        with mock.patch.object(APIException, '__init__', return_value=None):
            mock_register_device.side_effect = APIException(
                "msg",
                "content",
                "error_type",
                500
            )
        expected_response_data = b'response_json'

        app = get_app()
        with app.test_client() as c:
            actual_response = c.post("/api/device/register",
                                     headers={
                                         'x-api-key': 'Client test_key',
                                         'content-type': 'application/json'
                                     },
                                     json={'data': {}}
                                     )

        mock_service_init.assert_called_once_with()
        mock_register_device.assert_called_once_with({})
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)
