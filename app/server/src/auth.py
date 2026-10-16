"""
Responsible on auth side of service
"""
from functools import wraps

from flask import request

from src.config import Config
from src.client.service import ClientSessionService
from src.responses import SecurityException, APIException
from src.services.auth_service import AuthServices


def validate(
        is_auth_mandatory: bool = True,
        is_required: bool = True,
        resource: str = "",
        permission: str = ""):
    """
    :param is_auth_mandatory:
    :type is_auth_mandatory:
    :param is_required:
    :type is_required:
    :param resource:
    :type resource:
    :param permission:
    :type permission:
    :return:
    :rtype:
    """

    def check(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            record_id = kwargs.get("r_id", "")
            try:
                client_header = request.headers.get("x-api-key", "")
                client_token = (
                    client_header.removeprefix("Client ").strip()
                    if client_header.startswith("Client ") else ""
                )
                client_authenticated = bool(
                    client_token and ClientSessionService.authenticate_request(
                        client_token,
                        request.headers.get("X-Client-Installation", ""),
                        request.headers.get("X-Client-Platform", ""),
                        request.headers.get("X-Client-Timestamp", ""),
                        request.headers.get("X-Client-Request-Id", ""),
                        request.headers.get("X-Client-Signature", ""),
                        request.method,
                        request.path,
                        b"" if request.mimetype == "multipart/form-data"
                        else request.get_data(cache=True),
                    )
                )
                if not client_authenticated:
                    raise SecurityException('Client', 'Not Authenticated')

                if is_required:
                    authorization = request.headers.get("Authorization", "")
                    token = (
                        authorization.removeprefix("Bearer ").strip()
                        if authorization.startswith("Bearer ")
                        else request.headers.get('x-access-key', "")
                    )
                    if is_auth_mandatory and token == "":
                        raise SecurityException('User Token', 'Not found')

                    if token != "":
                        id_token, access_token = Config.get_tokens(token)
                        user_id = AuthServices().validate_token(id_token, access_token, resource, record_id, permission)

                    else:
                        user_id = None
                    return func(*args, **kwargs, user_id=user_id)
                return func(*args, **kwargs)
            except APIException as e:
                return e.get_response_json()

        return decorated

    return check
