"""
Responsible on auth side of service
"""
from functools import wraps

from flask import request

from src.services.auth_service import AuthServices
from src.config import Config
from src.responses import SecurityException, APIException


def validate(is_required: bool = True, resource: str = "", permission: str = ""):
    """
    :param is_required:
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
            client_key = request.headers.get('x-api-key')
            record_id = kwargs.get("r_id", "")
            try:
                if client_key not in Config.get_api_keys():
                    raise SecurityException('Client', 'Not Authenticated')

                if is_required:
                    token = request.headers.get('x-access-key', "")
                    if token == "":
                        raise SecurityException('User Token', 'Not found')

                    id_token, access_token = Config.get_tokens(token)
                    user_id = AuthServices().validate_token(id_token, access_token, resource, record_id, permission)
                    return func(*args, **kwargs, user_id=user_id)
                return func(*args, **kwargs)
            except APIException as e:
                return e.get_response_json()

        return decorated

    return check