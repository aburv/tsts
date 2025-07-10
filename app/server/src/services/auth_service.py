# pylint: skip-file
"""
Auth
"""

import grpc

from authentication_pb2 import LoginRequest, ValidateTokenRequest, RefreshTokenRequest
from authentication_pb2_grpc import AuthenticationServiceStub
from src.config import Config
from src.responses import RuntimeException, SecurityException


class AuthServices:
    """
    Calls to Auth Service
    """

    def __init__(self):
        channel = grpc.insecure_channel(
            Config.get_auth_connection_string()
        )

        self.client = AuthenticationServiceStub(channel)

    def login(self, user_id: str) -> (str, str):
        """
        Login call
        """
        try:
            login_request = LoginRequest(userId=user_id)
            response = self.client.Login(
                login_request,
            )
            return response.idToken, response.accessToken
        except grpc.RpcError as e:
            raise RuntimeException("Error in authenticating", f"{e}") from e

    def validate_token(self, id_token: str, token: str, resource: str, record_id: str, permission: str) -> str:
        """
        Token validation call
        """
        try:
            validate_request = ValidateTokenRequest(
                idToken=id_token,
                accessToken=token,
                objectKey=resource,
                recordId=record_id,
                permission=permission
            )
            response = self.client.ValidateToken(validate_request)
            return response.userId
        except grpc.RpcError as e:
            if self.check_for_is_unauthenticated(e):
                raise SecurityException("Invalid Token", "AccessToken")
            raise RuntimeException("Error in validating", f"{e}") from e

    @staticmethod
    def check_for_is_unauthenticated(e):
        return e.code() == grpc.StatusCode.UNAUTHENTICATED  # pragma: no cover

    def refresh_token(self, id_token: str, access_token: str) -> (str, str):
        """
        Refresh Token
        """
        try:
            refresh_request = RefreshTokenRequest(idToken=id_token, accessToken=access_token)
            response = self.client.RefreshToken(refresh_request)
            return response.idToken, response.accessToken
        except grpc.RpcError as e:
            raise RuntimeException("Error in refreshing", f"{e}") from e
