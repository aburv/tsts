"""
Caching Redis Config
"""
from functools import wraps

from flask import Flask, Response
from flask_caching import Cache

from src.config import Config
from src.responses import APIException, CachedResponse, ValidResponse


def get_if_cached(api_key: str, timeout=60):
    """
    Decorator checks with cache
    """

    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            param = '/'.join([f"{key}:{value}" for key, value in kwargs.items()])
            key = f"{RedisConfig.CACHE_KEY_PREFIX}{api_key}/{param}"

            cached_data = Caching.CACHE.get(key)
            if cached_data is not None:
                if isinstance(cached_data, bytes):
                    return Response(cached_data, mimetype='image/png')
                return CachedResponse(
                    key=key,
                    data=cached_data
                ).get_response_json()
            try:
                result: ValidResponse | bytes = func(*args, **kwargs)
                if isinstance(result, bytes):
                    Caching.CACHE.set(key, result, timeout=timeout)
                    return Response(result, mimetype='image/png')
                Caching.CACHE.set(key, result.get_data(), timeout=timeout)
                return result.get_response_json()
            except APIException as e:
                return e.get_response_json()

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
        app.config.from_object(RedisConfig)
        Caching.CACHE.init_app(app)


class RedisConfig:
    """
    Redis DB Config
    """
    CACHE_TYPE = 'redis'
    CACHE_KEY_PREFIX = 'myapp:'  # Optional: Prefix for cache keys

    @staticmethod
    def get_cache_url():
        """
        Frames redis cache url
        """
        params = Config.get_caching_parameters()
        return f'redis://{params.get("pass")}@{params.get("host")}:{params.get("port")}/0'

    CACHE_REDIS_URL = get_cache_url()

    # openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out cert.pem
# cache.delete(f'{Config.CACHE_KEY_PREFIX}:data/{i_id}')
