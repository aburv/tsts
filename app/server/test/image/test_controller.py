import unittest
from io import BytesIO
from unittest import mock

from werkzeug.datastructures.file_storage import FileStorage

from src.app import APP
from src.config import Config
from src.image.service import ImageServices
from src.responses import ValidResponse, APIException


class ImageControllerTest(unittest.TestCase):

    @mock.patch.object(ValidResponse, 'get_response_json', return_value='response_json')
    @mock.patch.object(ValidResponse, '__init__', return_value=None)
    @mock.patch.object(ImageServices, '__init__', return_value=None)
    @mock.patch.object(ImageServices, 'add', return_value='image_id')
    @mock.patch.object(Config, 'get_api_keys')
    def test_should_return_valid_image_id_response_on_add(self,
                                                          mock_secret_config,
                                                          mock_add,
                                                          mock_service_init,
                                                          mock_response_init,
                                                          mock_response
                                                          ):
        mock_secret_config.return_value = ['test_key']
        expected_response_data = b'response_json'

        data = BytesIO(b'This is a test file.')
        data.seek(0)
        file = (data, 'name.png', 'image/png')

        with APP.test_client() as c:
            actual_response = c.post("/api/image/add",
                                     headers={
                                         'x-api-key': 'test_key'
                                     },
                                     data={'file': file}
                                     )

            mock_service_init.assert_called_once_with()
            mock_add.assert_called_once()
            args, _ = mock_add.call_args
            self.assertIsInstance(args[0], FileStorage)
            self.assertEqual(args[1], "")
            mock_response_init.assert_called_once_with(domain='New image', detail="name.png", content='image_id')
            mock_response.assert_called_once_with()
            self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(APIException, 'get_response_json', return_value='response_json')
    @mock.patch.object(ImageServices, '__init__', return_value=None)
    @mock.patch.object(ImageServices, 'add', return_value='image_id')
    @mock.patch.object(Config, 'get_api_keys')
    def test_should_return_api_error_response_on_add(self,
                                                     mock_secret_config,
                                                     mock_add,
                                                     mock_service_init,
                                                     mock_response
                                                     ):
        mock_secret_config.return_value = ['test_key']
        with mock.patch.object(APIException, '__init__', return_value=None):
            mock_add.side_effect = APIException(
                "msg",
                "content",
                "error_type",
                500
            )
        expected_response_data = b'response_json'

        data = BytesIO(b'This is a test file.')
        data.seek(0)
        file = (data, 'name.png', 'image/png')

        with APP.test_client() as c:
            actual_response = c.post("/api/image/add",
                                     headers={
                                         'x-api-key': 'test_key'
                                     },
                                     data={'file': file}
                                     )

            mock_service_init.assert_called_once_with()
            mock_add.assert_called_once()
            args, _ = mock_add.call_args
            self.assertIsInstance(args[0], FileStorage)
            self.assertEqual(args[1], "")
            mock_response.assert_called_once_with()
            self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(ImageServices, '__init__', return_value=None)
    @mock.patch.object(ImageServices, 'get', return_value='image_id')
    @mock.patch.object(Config, 'get_api_keys')
    def test_should_return_valid_image_str_by_size_response_on_get(self,
                                                                   mock_secret_config,
                                                                   mock_add,
                                                                   mock_service_init
                                                                   ):
        mock_secret_config.return_value = ['test_key']
        expected_response_data = b'image_id'
        with APP.test_client() as c:
            actual_response = c.get("/api/image/image_id/size",
                                    headers={
                                        'x-api-key': 'test_key',
                                    }
                                    )

            mock_service_init.assert_called_once_with()
            mock_add.assert_called_once_with('image_id', 'size')
            self.assertEqual(actual_response.status_code, 200)
            self.assertEqual(actual_response.content_type, 'image/png')
            self.assertIsInstance(actual_response.data, bytes)
            self.assertGreater(len(actual_response.data), 0)
            self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(ImageServices, '__init__', return_value=None)
    @mock.patch.object(ImageServices, 'get', return_value='image_id')
    @mock.patch.object(Config, 'get_api_keys')
    def test_should_return_api_error_response_on_get_by_size(self,
                                                             mock_secret_config,
                                                             mock_get,
                                                             mock_service_init,
                                                             ):
        mock_secret_config.return_value = ['test_key']

        with mock.patch.object(APIException, '__init__', return_value=None):
            mock_get.side_effect = APIException(
                "msg",
                "content",
                "error_type",
                500
            )
        expected_response_data = b''
        with APP.test_client() as c:
            actual_response = c.get("/api/image/image_id/size",
                                    headers={
                                        'x-api-key': 'test_key',
                                    }
                                    )

            mock_service_init.assert_called_once_with()
            mock_get.assert_called_once_with('image_id', 'size')
            self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(ImageServices, '__init__', return_value=None)
    @mock.patch.object(ImageServices, 'get', return_value='image_id')
    @mock.patch.object(Config, 'get_api_keys')
    def test_should_return_valid_image_str_response_on_get(self,
                                                           mock_secret_config,
                                                           mock_add,
                                                           mock_service_init
                                                           ):
        mock_secret_config.return_value = ['test_key']
        expected_response_data = b'image_id'
        with APP.test_client() as c:
            actual_response = c.get("/api/image/image_id/",
                                    headers={
                                        'x-api-key': 'test_key',
                                    }
                                    )

            mock_service_init.assert_called_once_with()
            mock_add.assert_called_once_with('image_id', None)
            self.assertEqual(actual_response.status_code, 200)
            self.assertEqual(actual_response.content_type, 'image/png')
            self.assertIsInstance(actual_response.data, bytes)
            self.assertGreater(len(actual_response.data), 0)
            self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(ImageServices, '__init__', return_value=None)
    @mock.patch.object(ImageServices, 'get', return_value='image_id')
    @mock.patch.object(Config, 'get_api_keys')
    def test_should_return_api_error_response_on_get(self,
                                                     mock_secret_config,
                                                     mock_get,
                                                     mock_service_init,
                                                     ):
        mock_secret_config.return_value = ['test_key']

        with mock.patch.object(APIException, '__init__', return_value=None):
            mock_get.side_effect = APIException(
                "msg",
                "content",
                "error_type",
                500
            )
        expected_response_data = b''
        with APP.test_client() as c:
            actual_response = c.get("/api/image/image_id/",
                                    headers={
                                        'x-api-key': 'test_key',
                                    }
                                    )

            mock_service_init.assert_called_once_with()
            mock_get.assert_called_once_with('image_id', None)
            self.assertEqual(expected_response_data, actual_response.data)
