import unittest
from unittest.mock import patch, MagicMock

from flask import Flask

from src.caching import RedisConfig, Caching
from src.config import Config


class CacheConfigTest(unittest.TestCase):

    @patch.object(Flask, '__init__', return_value=None)
    def setUp(self, mock_flask):
        self.app = mock_flask

    @patch.object(Config, 'get_caching_parameters')
    def test_checks_Redis_config(self, mock_get_caching_params):
        mock_get_caching_params.return_value = {
            'user': 'user',
            'host': 'host',
            'port': 'port',
            'pass': 'pass'
        }

        url = "redis://user:pass@host:port/0"

        self.assertEqual(RedisConfig.get_cache_url(), url)

        self.assertEqual(RedisConfig.CACHE_TYPE, "redis")
        self.assertEqual(RedisConfig.CACHE_KEY_PREFIX, "myapp:")

    @patch('flask_caching.Cache.init_app', return_value=None)
    @patch.object(RedisConfig, 'CACHE_REDIS_URL', new_callable=MagicMock)
    @patch.object(RedisConfig, 'CACHE_KEY_PREFIX', new_callable=MagicMock)
    @patch.object(RedisConfig, 'CACHE_TYPE', new_callable=MagicMock)
    def test_cache_initialization(self, mock_type, mock_prefix, mock_redis_url, mock_cache_init):
        mock_redis_url.return_value = "url"
        mock_prefix.return_value = "prefix"
        mock_type.return_value = "type"

        Caching.init_cache(self.app)

        mock_cache_init.assert_called_once_with(self.app)
        self.app.config.from_object.assert_called_once_with(RedisConfig)

    @patch('flask_caching.Cache.init_app')
    @patch.object(RedisConfig, 'CACHE_REDIS_URL', new_callable=MagicMock)
    @patch.object(RedisConfig, 'CACHE_KEY_PREFIX', new_callable=MagicMock)
    @patch.object(RedisConfig, 'CACHE_TYPE', new_callable=MagicMock)
    def test_cache_initialization_failure(self, mock_type, mock_prefix, mock_redis_url, mock_cache_init):
        mock_redis_url.return_value = "url"
        mock_prefix.return_value = "prefix"
        mock_type.return_value = "type"

        mock_cache_init.side_effect = Exception("Cache initialization failed")

        with self.assertRaises(Exception) as context:
            Caching.init_cache(self.app)

        mock_cache_init.assert_called_once_with(self.app)
        self.app.config.from_object.assert_called_once_with(RedisConfig)

        self.assertTrue('Cache initialization failed' in str(context.exception))
