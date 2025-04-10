import unittest
from io import BytesIO
from unittest import mock

from werkzeug.datastructures.file_storage import FileStorage

from src.app import App
from src.caching import Caching
from src.config import Config
from src.image.service import ImageServices
from src.responses import ValidResponse, APIException, APIResponse, SecurityException
from src.services.auth_service import AuthServices


class ImageControllerTest(unittest.TestCase):

    @mock.patch.object(APIResponse, 'get_response_json', return_value='response_json')
    @mock.patch.object(ValidResponse, '__init__', return_value=None)
    @mock.patch.object(ImageServices, '__init__', return_value=None)
    @mock.patch.object(ImageServices, 'add', return_value='image_id')
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    def test_should_return_valid_image_id_response_on_add(self,
                                                          mock_get_tokens,
                                                          mock_secret_config,
                                                          mock_validate_token,
                                                          mock_auth_service,
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

        with mock.patch.object(Caching, 'init_cache'):
            app = App.create()
            with app.test_client() as c:
                actual_response = c.post("/api/image/add",
                                         headers={
                                             'x-api-key': 'test_key',
                                             'x-access-key': 'token'
                                         },
                                         data={'file': file}
                                         )

        mock_secret_config.assert_called_once_with()
        mock_get_tokens.assert_called_once_with('token')
        mock_auth_service.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', 'image', '', 'create')
        mock_service_init.assert_called_once_with()
        mock_add.assert_called_once()
        args, _ = mock_add.call_args
        self.assertIsInstance(args[0], FileStorage)
        self.assertEqual(args[1], "user_id")
        mock_response_init.assert_called_once_with(domain='New Image', detail="name.png", data='image_id')
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(APIException, 'get_response_json', return_value='response_json')
    @mock.patch.object(SecurityException, '__init__', return_value=None)
    @mock.patch.object(ImageServices, '__init__', return_value=None)
    @mock.patch.object(ImageServices, 'add', return_value='image_id')
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    def test_should_return_security_exception_response_when_no_access_token_on_add(self,
                                                                                   mock_get_tokens,
                                                                                   mock_secret_config,
                                                                                   mock_validate_token,
                                                                                   mock_auth_service,
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

        with mock.patch.object(Caching, 'init_cache'):
            app = App.create()
            with app.test_client() as c:
                actual_response = c.post("/api/image/add",
                                         headers={
                                             'x-api-key': 'test_key',
                                         },
                                         data={'file': file}
                                         )

        mock_secret_config.assert_called_once_with()
        assert not mock_get_tokens.called
        assert not mock_auth_service.called
        assert not mock_validate_token.called
        assert not mock_service_init.called
        assert not mock_add.called
        mock_response_init.assert_called_once_with('User Token', 'Not found')
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(APIException, 'get_response_json', return_value='response_json')
    @mock.patch.object(ImageServices, '__init__', return_value=None)
    @mock.patch.object(ImageServices, 'add', return_value='image_id')
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    def test_should_return_api_error_response_on_add(self,
                                                     mock_get_tokens,
                                                     mock_secret_config,
                                                     mock_validate_token,
                                                     mock_auth_service,
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

        with mock.patch.object(Caching, 'init_cache'):
            app = App.create()
            with app.test_client() as c:
                actual_response = c.post("/api/image/add",
                                         headers={
                                             'x-api-key': 'test_key',
                                             'x-access-key': 'token'
                                         },
                                         data={'file': file}
                                         )

        mock_secret_config.assert_called_once_with()
        mock_get_tokens.assert_called_once_with('token')
        mock_auth_service.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', 'image', '', 'create')
        mock_service_init.assert_called_once_with()
        mock_add.assert_called_once()
        args, _ = mock_add.call_args
        self.assertIsInstance(args[0], FileStorage)
        self.assertEqual(args[1], 'user_id')
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(ImageServices, '__init__', return_value=None)
    @mock.patch.object(ImageServices, 'get', return_value=b'image_str')
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch('flask_caching.Cache.get')
    @mock.patch('flask_caching.Cache.set')
    def test_should_return_valid_image_str_by_size_and_cache_response_on_get_image_by_size(self,
                                                                                           mock_cache_set,
                                                                                           mock_cache_get,
                                                                                           mock_secret_config,
                                                                                           mock_get,
                                                                                           mock_service_init
                                                                                           ):
        mock_cache_get.return_value = None

        mock_secret_config.return_value = ['test_key']
        expected_response_data = b'image_str'

        with mock.patch.object(Caching, 'init_cache'):
            app = App.create()
            with app.test_client() as c:
                actual_response = c.get("/api/image/image_id/size",
                                        headers={
                                            'x-api-key': 'test_key',
                                        }
                                        )

        mock_cache_get.assert_called_once_with('myapp:image/r_id:image_id/size:size')
        mock_cache_set.assert_called_once_with('myapp:image/r_id:image_id/size:size', b'image_str', timeout=60)
        mock_service_init.assert_called_once_with()
        mock_get.assert_called_once_with('image_id', 'size')
        self.assertEqual(actual_response.status_code, 200)
        self.assertEqual(actual_response.content_type, 'image/png')
        self.assertIsInstance(actual_response.data, bytes)
        self.assertGreater(len(actual_response.data), 0)
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(ImageServices, '__init__', return_value=None)
    @mock.patch.object(ImageServices, 'get')
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch('flask_caching.Cache.get')
    @mock.patch('flask_caching.Cache.set')
    def test_should_return_cached_image_str_by_size_response_on_get_image_by_size(self,
                                                                                  mock_cache_set,
                                                                                  mock_cache_get,
                                                                                  mock_secret_config,
                                                                                  mock_get,
                                                                                  mock_service_init
                                                                                  ):
        mock_cache_get.return_value = b'image_str'

        mock_secret_config.return_value = ['test_key']
        expected_response_data = b'image_str'

        with mock.patch.object(Caching, 'init_cache'):
            app = App.create()
            with app.test_client() as c:
                actual_response = c.get("/api/image/image_id/size",
                                        headers={
                                            'x-api-key': 'test_key',
                                        }
                                        )

        mock_cache_get.assert_called_once_with('myapp:image/r_id:image_id/size:size')
        assert not mock_cache_set.called
        assert not mock_service_init.called
        assert not mock_get.called
        self.assertEqual(actual_response.status_code, 200)
        self.assertEqual(actual_response.content_type, 'image/png')
        self.assertIsInstance(actual_response.data, bytes)
        self.assertGreater(len(actual_response.data), 0)
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(ImageServices, '__init__', return_value=None)
    @mock.patch.object(ImageServices, 'get')
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch('flask_caching.Cache.get')
    @mock.patch('flask_caching.Cache.set')
    def test_should_return_api_error_response_on_get_image_by_size(self,
                                                                   mock_cache_set,
                                                                   mock_cache_get,
                                                                   mock_secret_config,
                                                                   mock_get,
                                                                   mock_service_init,
                                                                   ):
        mock_cache_get.return_value = None
        mock_secret_config.return_value = ['test_key']

        with mock.patch.object(APIException, '__init__', return_value=None):
            mock_get.side_effect = APIException(
                "msg",
                "content",
                "error_type",
                500
            )
        expected_response_data = b''

        with mock.patch.object(Caching, 'init_cache'):
            app = App.create()
            with app.test_client() as c:
                actual_response = c.get("/api/image/image_id/size",
                                        headers={
                                            'x-api-key': 'test_key',
                                        }
                                        )

        mock_cache_get.assert_called_once_with('myapp:image/r_id:image_id/size:size')
        mock_cache_set.assert_called_once_with('myapp:image/r_id:image_id/size:size', b'', timeout=60)
        mock_service_init.assert_called_once_with()
        mock_get.assert_called_once_with('image_id', 'size')
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(ImageServices, '__init__', return_value=None)
    @mock.patch.object(ImageServices, 'get', return_value=b'image_str')
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    @mock.patch('flask_caching.Cache.get')
    @mock.patch('flask_caching.Cache.set')
    def test_should_return_valid_image_str_and_cache_response_on_get_original_image(self,
                                                                                    mock_cache_set,
                                                                                    mock_cache_get,
                                                                                    mock_get_tokens,
                                                                                    mock_secret_config,
                                                                                    mock_validate_token,
                                                                                    mock_auth_service,
                                                                                    mock_get,
                                                                                    mock_service_init
                                                                                    ):
        mock_cache_get.return_value = None
        mock_secret_config.return_value = ['test_key']
        expected_response_data = b'image_str'

        with mock.patch.object(Caching, 'init_cache'):
            app = App.create()
            with app.test_client() as c:
                actual_response = c.get("/api/image/image_id/",
                                        headers={
                                            'x-api-key': 'test_key',
                                            'x-access-key': 'token',
                                        }
                                        )

        mock_cache_get.assert_called_once_with('myapp:image/r_id:image_id/user_id:user_id')
        mock_cache_set.assert_called_once_with('myapp:image/r_id:image_id/user_id:user_id', b'image_str', timeout=60)
        mock_secret_config.assert_called_once_with()
        mock_get_tokens.assert_called_once_with('token')
        mock_auth_service.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', 'image', 'image_id', 'view')
        mock_service_init.assert_called_once_with()
        mock_get.assert_called_once_with('image_id', None)
        self.assertEqual(actual_response.status_code, 200)
        self.assertEqual(actual_response.content_type, 'image/png')
        self.assertIsInstance(actual_response.data, bytes)
        self.assertGreater(len(actual_response.data), 0)
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(ImageServices, '__init__', return_value=None)
    @mock.patch.object(ImageServices, 'get')
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    @mock.patch('flask_caching.Cache.get')
    @mock.patch('flask_caching.Cache.set')
    def test_should_return_cached_image_str_response_on_get_original_image(self,
                                                                           mock_cache_set,
                                                                           mock_cache_get,
                                                                           mock_get_tokens,
                                                                           mock_secret_config,
                                                                           mock_validate_token,
                                                                           mock_auth_service,
                                                                           mock_get,
                                                                           mock_service_init
                                                                           ):
        mock_cache_get.return_value = b'image_str'

        mock_secret_config.return_value = ['test_key']
        expected_response_data = b'image_str'

        with mock.patch.object(Caching, 'init_cache'):
            app = App.create()
            with app.test_client() as c:
                actual_response = c.get("/api/image/image_id/",
                                        headers={
                                            'x-api-key': 'test_key',
                                            'x-access-key': 'token',
                                        }
                                        )

        mock_cache_get.assert_called_once_with('myapp:image/r_id:image_id/user_id:user_id')
        mock_secret_config.assert_called_once_with()
        mock_get_tokens.assert_called_once_with('token')
        mock_auth_service.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', 'image', 'image_id', 'view')
        assert not mock_cache_set.called
        assert not mock_service_init.called
        assert not mock_get.called
        self.assertEqual(actual_response.status_code, 200)
        self.assertEqual(actual_response.content_type, 'image/png')
        self.assertIsInstance(actual_response.data, bytes)
        self.assertGreater(len(actual_response.data), 0)
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(ImageServices, '__init__', return_value=None)
    @mock.patch.object(ImageServices, 'get')
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    @mock.patch('flask_caching.Cache.get')
    @mock.patch('flask_caching.Cache.set')
    def test_should_return_api_error_response_on_get_original_image(self,
                                                                    mock_cache_set,
                                                                    mock_cache_get,
                                                                    mock_get_tokens,
                                                                    mock_secret_config,
                                                                    mock_validate_token,
                                                                    mock_auth_service,
                                                                    mock_get,
                                                                    mock_service_init,
                                                                    ):
        mock_cache_get.return_value = None
        mock_secret_config.return_value = ['test_key']

        with mock.patch.object(APIException, '__init__', return_value=None):
            mock_get.side_effect = APIException(
                "msg",
                "content",
                "error_type",
                500
            )
        expected_response_data = b''

        with mock.patch.object(Caching, 'init_cache'):
            app = App.create()
            with app.test_client() as c:
                actual_response = c.get("/api/image/image_id/",
                                        headers={
                                            'x-api-key': 'test_key',
                                            'x-access-key': 'token',
                                        }
                                        )

        mock_cache_get.assert_called_once_with('myapp:image/r_id:image_id/user_id:user_id')
        mock_cache_set.assert_called_once_with('myapp:image/r_id:image_id/user_id:user_id', b'', timeout=60)
        mock_secret_config.assert_called_once_with()
        mock_get_tokens.assert_called_once_with('token')
        mock_auth_service.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', 'image', 'image_id', 'view')
        mock_service_init.assert_called_once_with()
        mock_get.assert_called_once_with('image_id', None)
        self.assertEqual(expected_response_data, actual_response.data)
