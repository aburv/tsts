import unittest
from io import BytesIO
from unittest import mock

from werkzeug.datastructures import FileStorage

from src.config import Config
from src.client.service import ClientSessionService
from src.responses import ValidResponse, APIException, APIResponse, CachedResponse
from src.services.auth_service import AuthServices
from src.user.service import UserServices
from src.image.service import ImageServices
from test.test_app_config import get_app


class UserControllerTest(unittest.TestCase):

    @mock.patch.object(APIResponse, 'get_response_json', return_value='response_json')
    @mock.patch.object(ValidResponse, '__init__', return_value=None)
    @mock.patch.object(ValidResponse, 'get_data', return_value={})
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_user_data', return_value={})
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(ClientSessionService, 'authenticate_request')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    @mock.patch('flask_caching.Cache.get')
    @mock.patch('flask_caching.Cache.set')
    def test_should_return_valid_user_data_and_cache_response(self,
                                                              mock_cache_set,
                                                              mock_cache_get,
                                                              mock_get_tokens,
                                                              mock_authenticate_request,
                                                              mock_validate_token,
                                                              mock_auth_service,
                                                              mock_user_data,
                                                              mock_service,
                                                              mock_response_get_data,
                                                              mock_response_init,
                                                              mock_response
                                                              ):
        mock_cache_get.return_value = None

        mock_authenticate_request.return_value = 'test_key'
        expected_response_data = b'response_json'

        app = get_app()
        with app.test_client() as c:
            actual_response = c.get(
                "/api/user/app",
                headers={'x-api-key': 'Client test_key', 'x-access-key': 'token'},
            )

        mock_cache_get.assert_called_once_with('myapp:app_user/user_id:user_id')
        mock_cache_set.assert_called_once_with('myapp:app_user/user_id:user_id', {}, timeout=60)
        
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
    @mock.patch.object(ClientSessionService, 'authenticate_request')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    @mock.patch('flask_caching.Cache.get')
    @mock.patch('flask_caching.Cache.set')
    def test_should_return_valid_user_data_and_cache_response_when_no_access_token(self,
                                                                                   mock_cache_set,
                                                                                   mock_cache_get,
                                                                                   mock_get_tokens,
                                                                                   mock_authenticate_request,
                                                                                   mock_validate_token,
                                                                                   mock_auth_service,
                                                                                   mock_user_data,
                                                                                   mock_service,
                                                                                   mock_response_get_data,
                                                                                   mock_response_init,
                                                                                   mock_response
                                                                                   ):
        mock_cache_get.return_value = None

        mock_authenticate_request.return_value = 'test_key'
        expected_response_data = b'response_json'

        app = get_app()
        with app.test_client() as c:
            actual_response = c.get(
                "/api/user/app",
                headers={'x-api-key': 'Client test_key'},
            )

        mock_cache_get.assert_called_once_with('')
        assert not mock_cache_set.called
        
        assert not mock_get_tokens.called
        assert not mock_auth_service.called
        assert not mock_validate_token.called
        mock_service.assert_called_once_with()
        mock_user_data.assert_called_once_with(None)
        assert not mock_response_get_data.called
        mock_response_init.assert_called_once_with(domain='Retrieved user data', detail=None, data={})
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(APIResponse, 'get_response_json', return_value='response_json')
    @mock.patch.object(CachedResponse, '__init__', return_value=None)
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_user_data', return_value={})
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(ClientSessionService, 'authenticate_request')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    @mock.patch('flask_caching.Cache.get')
    @mock.patch('flask_caching.Cache.set')
    def test_should_return_cached_user_data_response(self,
                                                     mock_cache_set,
                                                     mock_cache_get,
                                                     mock_get_tokens,
                                                     mock_authenticate_request,
                                                     mock_validate_token,
                                                     mock_auth_service,
                                                     mock_user_data,
                                                     mock_service,
                                                     mock_response_init,
                                                     mock_response
                                                     ):
        mock_cache_get.return_value = {}

        mock_authenticate_request.return_value = 'test_key'
        expected_response_data = b'response_json'

        app = get_app()
        with app.test_client() as c:
            actual_response = c.get(
                "/api/user/app",
                headers={'x-api-key': 'Client test_key', 'x-access-key': 'token'},
            )

        mock_cache_get.assert_called_once_with('myapp:app_user/user_id:user_id')
        assert not mock_cache_set.called
        assert not mock_service.called
        assert not mock_user_data.called
        
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
    @mock.patch.object(ClientSessionService, 'authenticate_request')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    @mock.patch('flask_caching.Cache.get')
    @mock.patch('flask_caching.Cache.set')
    def test_should_return_error_response_on_get_user(self,
                                                      mock_cache_set,
                                                      mock_cache_get,
                                                      mock_get_tokens,
                                                      mock_authenticate_request,
                                                      mock_validate_token,
                                                      mock_auth_service,
                                                      mock_user_data,
                                                      mock_service,
                                                      mock_response
                                                      ):
        mock_cache_get.return_value = None

        mock_authenticate_request.return_value = 'test_key'

        with mock.patch.object(APIException, '__init__', return_value=None):
            mock_user_data.side_effect = APIException(
                "msg",
                "content",
                "error_type",
                500
            )
        expected_response_data = b'response_json'

        app = get_app()
        with app.test_client() as c:
            actual_response = c.get(
                "/api/user/app",
                headers={'x-api-key': 'Client test_key', 'x-access-key': 'token'},
            )

        mock_cache_get.assert_called_once_with('myapp:app_user/user_id:user_id')
        assert not mock_cache_set.called
        
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
    @mock.patch.object(ClientSessionService, 'authenticate_request')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    def test_should_return_t_valid_response_on_set_done_onboarding(self,
                                                                   mock_get_tokens,
                                                                   mock_authenticate_request,
                                                                   mock_validate_token,
                                                                   mock_auth_service,
                                                                   mock_done_user_onboarding,
                                                                   mock_service,
                                                                   mock_response_init,
                                                                   mock_response
                                                                   ):
        mock_authenticate_request.return_value = 'test_key'
        expected_response_data = b'response_json'

        app = get_app()
        with app.test_client() as c:
            actual_response = c.post(
                "/api/user/done_onboarding",
                json={'data': {}},
                headers={'x-api-key': 'Client test_key', 'x-access-key': 'token'},
            )

        mock_get_tokens.assert_called_once_with('token')
        mock_auth_service.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', '', '', '')
        mock_service.assert_called_once_with()
        mock_done_user_onboarding.assert_called_once_with('user_id')
        mock_response_init.assert_called_once_with(domain='Done user onboarding', detail='user_id', data='t')
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(ValidResponse, 'get_response_json', return_value={"data": ""})
    @mock.patch.object(ValidResponse, '__init__', return_value=None)
    @mock.patch.object(APIException, '__init__', return_value=None)
    @mock.patch.object(ImageServices, 'add', return_value='image_id')
    @mock.patch.object(ImageServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'update_image', return_value=True)
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(ClientSessionService, 'authenticate_request', return_value=True)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    def test_should_return_empty_response_when_update_image_fails(self,
                                                                  mock_get_tokens,
                                                                  mock_auth_service,
                                                                  mock_validate_token,
                                                                  mock_authenticate_request,
                                                                  mock_user_init,
                                                                  mock_update,
                                                                  mock_image_init,
                                                                  mock_add,
                                                                  mock_exception,
                                                                  mock_response_init,
                                                                  mock_response):
        mock_update.side_effect = Exception("error")
        app = get_app()
        with app.test_client() as c:
            actual_response = c.post(
                '/api/user/image',
                headers={'x-api-key': 'Client test_key', 'x-access-key': 'token'},
                data={'file': (BytesIO(b'image'), 'image.png')},
                content_type='multipart/form-data'
            )
        mock_authenticate_request.assert_called_once_with(
            'test_key', '', '', '', '', '', 'POST', '/api/user/image', b''
        )
        mock_get_tokens.assert_called_once_with('token')
        mock_auth_service.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', '', '', '')
        mock_image_init.assert_called_once_with()
        mock_add.assert_called_once()
        args, _ = mock_add.call_args
        self.assertIsInstance(args[0], FileStorage)
        self.assertEqual(args[1], 'user_id')
        mock_user_init.assert_called_once_with()
        mock_update.assert_called_once_with('image_id', 'user_id')
        mock_exception.assert_called_once_with('Update the image', 'error', '', '', is_error=False)
        mock_response_init.assert_called_once_with(
            domain='Update the image', detail='user_id', data=""
        )
        mock_response.assert_called_once_with()
        self.assertEqual(b'{"data":""}\n', actual_response.data)

    @mock.patch.object(ValidResponse, 'get_response_json', return_value={"data": "image_id"})
    @mock.patch.object(ValidResponse, '__init__', return_value=None)
    @mock.patch.object(ImageServices, 'add', return_value='image_id')
    @mock.patch.object(ImageServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'update_image', return_value=True)
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(ClientSessionService, 'authenticate_request', return_value=True)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    def test_should_return_image_id_when_update_image_succeeds(self,
                                                               mock_get_tokens,
                                                               mock_auth_service,
                                                               mock_validate_token,
                                                               mock_authenticate_request,
                                                               mock_user_init,
                                                               mock_update,
                                                               mock_image_init,
                                                               mock_add,
                                                               mock_response_init,
                                                               mock_response
                                                               ):
        app = get_app()
        with app.test_client() as c:
            actual_response = c.post(
                '/api/user/image',
                headers={'x-api-key': 'Client test_key', 'x-access-key': 'token'},
                data={'file': (BytesIO(b'image'), 'image.png')},
                content_type='multipart/form-data'
            )
        mock_authenticate_request.assert_called_once_with(
            'test_key', '', '', '', '', '', 'POST', '/api/user/image', b''
        )
        mock_get_tokens.assert_called_once_with('token')
        mock_auth_service.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', '', '', '')
        mock_image_init.assert_called_once_with()
        mock_add.assert_called_once()
        args, _ = mock_add.call_args
        self.assertIsInstance(args[0], FileStorage)
        self.assertEqual(args[1], 'user_id')
        mock_user_init.assert_called_once_with()
        mock_update.assert_called_once_with('image_id', 'user_id')
        mock_response_init.assert_called_once_with(
            domain='Updated the image', detail='user_id', data='image_id'
        )
        mock_response.assert_called_once_with()
        self.assertEqual(b'{"data":"image_id"}\n', actual_response.data)
