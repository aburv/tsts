import unittest
from unittest import mock
from unittest.mock import MagicMock

import grpc
from grpc import Channel

from authentication_pb2 import LoginRequest, ValidateTokenRequest, RefreshTokenRequest
from authentication_pb2_grpc import AuthenticationServiceStub
from src.config import Config
from src.responses import RuntimeException, SecurityException
from src.services.auth_service import AuthServices


class AuthServicesTest(unittest.TestCase):

    @mock.patch.object(AuthenticationServiceStub, "__init__", return_value=None)
    @mock.patch.object(Channel, "__init__", return_value=None)
    @mock.patch("grpc.insecure_channel")
    @mock.patch.object(Config, "get_auth_connection_string", return_value="connection_string")
    def test_should_init_auth_services(self,
                                       mock_get_auth_connection_string,
                                       mock_insecure_channel,
                                       mock_channel,
                                       mock_stub):
        mock_insecure_channel.return_value = mock_channel

        services = AuthServices()

        mock_get_auth_connection_string.assert_called_once_with()
        mock_insecure_channel.assert_called_once_with('connection_string')
        mock_stub.assert_called_once_with(mock_channel)
        self.assertIsInstance(services.client, AuthenticationServiceStub)

    @mock.patch.object(LoginRequest, "__init__", return_value=None)
    @mock.patch.object(AuthenticationServiceStub, "__init__", return_value=None)
    def test_should_return_token_on_login(self, mock_client, mock_request):
        mock_response = MagicMock()
        mock_response.idToken = "id_token"
        mock_response.accessToken = "access_token"
        mock_client.Login.return_value = mock_response

        with mock.patch.object(AuthServices, "__init__", return_value=None):
            services = AuthServices()
            services.client = mock_client

        actual = services.login("user_id")

        mock_request.assert_called_once_with(userId='user_id')
        # mock_client.Login.assert_called_once_with(mock_request)

        self.assertEqual(actual, ('id_token', 'access_token'))

    @mock.patch.object(ValidateTokenRequest, "__init__", return_value=None)
    @mock.patch.object(AuthenticationServiceStub, "__init__", return_value=None)
    def test_should_return_user_id_on_validate_token(self, mock_client, mock_request):
        mock_response = MagicMock()
        mock_response.userId = "user_id"
        mock_client.ValidateToken.return_value = mock_response

        with mock.patch.object(AuthServices, "__init__", return_value=None):
            services = AuthServices()
            services.client = mock_client

        actual = services.validate_token("id_token", 'access_token', '', '', '')

        mock_request.assert_called_once_with(idToken='id_token', accessToken='access_token', objectKey='',
                                             recordId='', permission='')
        # mock_client.ValidateToken.assert_called_once_with(mock_request)

        self.assertEqual(actual, "user_id")

    @mock.patch.object(RefreshTokenRequest, "__init__", return_value=None)
    @mock.patch.object(AuthenticationServiceStub, "__init__", return_value=None)
    def test_should_return_refresh_token_on_refresh_token(self, mock_client, mock_request):
        mock_response = MagicMock()
        mock_response.idToken = "id_token"
        mock_response.accessToken = "access_token"
        mock_client.RefreshToken.return_value = mock_response

        with mock.patch.object(AuthServices, "__init__", return_value=None):
            services = AuthServices()
            services.client = mock_client

        actual = services.refresh_token("id_token", "access_token")

        mock_request.assert_called_once_with(idToken='id_token', accessToken='access_token')
        # mock_client.RefreshToken.assert_called_once_with(mock_request)

        self.assertEqual(("id_token", "access_token"), actual)

    @mock.patch.object(RuntimeException, "__init__", return_value=None)
    @mock.patch.object(LoginRequest, "__init__", return_value=None)
    @mock.patch.object(AuthenticationServiceStub, "__init__", return_value=None)
    def test_should_raise_runtime_error_on_login(self, mock_client, mock_request, mock_exception):
        mock_client.Login.side_effect = grpc.RpcError('error')

        with mock.patch.object(AuthServices, "__init__", return_value=None):
            services = AuthServices()
            services.client = mock_client

        with self.assertRaises(RuntimeException):
            services.login("user_id")

        mock_request.assert_called_once_with(userId='user_id')
        # mock_client.Login.assert_called_once_with(mock_request)

        mock_exception.assert_called_once_with('Error in authenticating', 'error')

    @mock.patch.object(RuntimeException, "__init__", return_value=None)
    @mock.patch.object(ValidateTokenRequest, "__init__", return_value=None)
    @mock.patch.object(AuthenticationServiceStub, "__init__", return_value=None)
    @mock.patch.object(AuthServices, "check_for_is_unauthenticated", return_value=False)
    def test_should_raise_runtime_error_on_validate_token(self,
                                                          mock_check_for_is_unauthenticated,
                                                          mock_client,
                                                          mock_request,
                                                          mock_exception
                                                          ):
        mock_client.ValidateToken.side_effect = grpc.RpcError('error')

        with mock.patch.object(AuthServices, "__init__", return_value=None):
            services = AuthServices()
            services.client = mock_client

        with self.assertRaises(RuntimeException):
            services.validate_token("id_token", 'access_token', '', '', '')

        mock_request.assert_called_once_with(idToken='id_token', accessToken='access_token', objectKey='',
                                             recordId='', permission='')
        # mock_client.ValidateToken.assert_called_once_with(mock_request)
        mock_check_for_is_unauthenticated.assert_called_once()
        mock_exception.assert_called_once_with('Error in validating', 'error')

    @mock.patch.object(SecurityException, "__init__", return_value=None)
    @mock.patch.object(ValidateTokenRequest, "__init__", return_value=None)
    @mock.patch.object(AuthenticationServiceStub, "__init__", return_value=None)
    @mock.patch.object(AuthServices, "check_for_is_unauthenticated", return_value=True)
    def test_should_raise_security_exception_on_validate_token(self,
                                                               mock_check_for_is_unauthenticated,
                                                               mock_client,
                                                               mock_request,
                                                               mock_exception
                                                               ):
        mock_client.ValidateToken.side_effect = grpc.RpcError('error')

        with mock.patch.object(AuthServices, "__init__", return_value=None):
            services = AuthServices()
            services.client = mock_client

        with self.assertRaises(SecurityException):
            services.validate_token("id_token", 'access_token', '', '', '')

        mock_request.assert_called_once_with(idToken='id_token', accessToken='access_token', objectKey='',
                                             recordId='', permission='')
        # mock_client.ValidateToken.assert_called_once_with(mock_request)
        mock_check_for_is_unauthenticated.assert_called_once()
        mock_exception.assert_called_once_with('Invalid Token', 'AccessToken')

    @mock.patch.object(RuntimeException, "__init__", return_value=None)
    @mock.patch.object(RefreshTokenRequest, "__init__", return_value=None)
    @mock.patch.object(AuthenticationServiceStub, "__init__", return_value=None)
    def test_should_raise_runtime_error_on_refresh_token(self, mock_client, mock_request, mock_exception):
        mock_client.RefreshToken.side_effect = grpc.RpcError('error')

        with mock.patch.object(AuthServices, "__init__", return_value=None):
            services = AuthServices()
            services.client = mock_client

        with self.assertRaises(RuntimeException):
            services.refresh_token("id_token", "access_token")

        mock_request.assert_called_once_with(idToken='id_token', accessToken='access_token')
        # mock_client.RefreshToken.assert_called_once_with(mock_request)

        mock_exception.assert_called_once_with('Error in refreshing', 'error')
