"""
Caching Redis Config
"""
from functools import wraps
from urllib.parse import quote

from flask import Flask, Response
from flask_caching import Cache

from src.config import Config
from src.responses import APIException, CachedResponse, ValidResponse


def get_if_cached(api_key: str, timeout=60, user_specific=True, needs_user=True):
    """
    Decorator checks with cache
    """

    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if needs_user and kwargs["user_id"] is None:
                key = ""
            else:
                param = '/'.join(
                    f"{key}:{value}"
                    for key, value in kwargs.items()
                    if user_specific or (key != "user_id" or value is not None)
                )
                key = f"{RedisConfig.CACHE_KEY_PREFIX}{api_key}/{param}"
            try:
                cached_data = Caching.CACHE.get(key)
            except Exception as e:
                cached_data = None
            if cached_data is not None:
                if isinstance(cached_data, bytes):
                    return Response(cached_data, mimetype='image/png')
                return CachedResponse(
                    key=key,
                    data=cached_data
                ).get_response_json()
            try:
                result: ValidResponse | bytes = func(*args, **kwargs)
            except APIException as e:
                return e.get_response_json()
            if key != "":
                if isinstance(result, bytes):
                    if result != b'':
                        try:
                            Caching.CACHE.set(key, result, timeout=timeout)
                        except Exception as e:
                            pass
                    return Response(result, mimetype='image/png')
                else:
                    try:
                        Caching.CACHE.set(key, result.get_data(), timeout=timeout)
                    except Exception as e:
                        pass
            return result.get_response_json()

        return wrapped

    return decorator


class Caching:
    """
    Cache Interface
    """
    CACHE = Cache()

    @staticmethod
    def init_cache(app: Flask):
        """
        Initializing cache to app
        """
        try:
            app.config.from_object(RedisConfig)
            if RedisConfig.CACHE_REDIS_URL is None:
                app.config["CACHE_REDIS_URL"] = RedisConfig.get_cache_url()
            Caching.CACHE.init_app(app)
        except Exception as e:
            pass


class RedisConfig:
    """
    Redis DB Config
    """
    CACHE_TYPE = 'redis'
    CACHE_KEY_PREFIX = 'myapp:'

    @staticmethod
    def get_cache_url():
        """
        Frames redis cache url
        """
        params = Config.get_caching_parameters()
        host = params.get("host")
        port = params.get("port")
        username = params.get("user")
        password = params.get("pass")
        credentials = ""
        if password:
            credentials = f":{quote(password)}@"
            if username:
                credentials = f"{quote(username)}:{quote(password)}@"
        return f"redis://{credentials}{host}:{port}/0"

    CACHE_REDIS_URL = None
