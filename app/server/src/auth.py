"""
 Responsible on auth side of service
"""
from functools import wraps

from flask import request

from src.config import Config
from src.responses import SecurityException


def client_auth(func):
    """
    :param func:
    :type func:
    :return:
    :rtype:
    """

    @wraps(func)
    def decorated(*args, **kwargs):
        client_key = request.headers.get('x-api-key')

        if client_key not in Config.get_api_keys():
            return SecurityException('Client', 'Not Authenticated').get_response_json()

        return func(*args, **kwargs)

    return decorated
