import os
import unittest
from unittest import mock

from src.config import Config
from src.secret_manager import (
    EnvironmentSecretProvider,
    SecretProviderFactory,
    SecretStore,
    _decode_secret,
)


class SecretManagerTest(unittest.TestCase):

    @mock.patch.dict(os.environ, {"POSTGRES_PASSWORD": "password"}, clear=True)
    def test_environment_provider_reads_value_directly(self):
        provider = EnvironmentSecretProvider()

        self.assertEqual(
            {"POSTGRES_PASSWORD": "password"},
            provider.get_secret("POSTGRES_PASSWORD"),
        )

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_environment_provider_rejects_missing_value(self):
        with self.assertRaisesRegex(ValueError, "POSTGRES_PASSWORD.*not set"):
            EnvironmentSecretProvider().get_secret("POSTGRES_PASSWORD")

    @mock.patch.dict(os.environ, {"SECRET_PROVIDER": "env", "SECRET_NAME": "POSTGRES_PASSWORD",
                                  "POSTGRES_PASSWORD": "password"}, clear=True)
    def test_factory_creates_environment_provider(self):
        provider = SecretProviderFactory.create()

        self.assertEqual({"POSTGRES_PASSWORD": "password"}, provider.get_secret("POSTGRES_PASSWORD"))

    @mock.patch.dict(os.environ, {"SECRET_PROVIDER": " ENV "}, clear=True)
    def test_factory_accepts_case_and_whitespace(self):
        self.assertIsInstance(SecretProviderFactory.create(), EnvironmentSecretProvider)

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_factory_rejects_missing_provider(self):
        with self.assertRaisesRegex(ValueError, "SECRET_PROVIDER"):
            SecretProviderFactory.create()

    @mock.patch.dict(os.environ, {"SECRET_PROVIDER": "vault"}, clear=True)
    def test_factory_rejects_unsupported_provider(self):
        with self.assertRaisesRegex(ValueError, "SECRET_PROVIDER"):
            SecretProviderFactory.create()

    @mock.patch.dict(os.environ, {"SECRET_PROVIDER": "aws", "SECRET_NAME": "app-credentials"}, clear=True)
    @mock.patch.object(SecretProviderFactory, "create")
    def test_config_reads_credentials_from_configured_provider(self, create_provider):
        provider = mock.Mock()
        provider.get_secret.return_value = {
            "POSTGRES_DB": "database",
            "POSTGRES_PASSWORD": "password",
            "POSTGRES_USER": "user",
            "POSTGRES_HOST": "host",
            "POSTGRES_PORT": "5432",
            "POSTGRES_SCHEMA_META": "meta",
            "POSTGRES_SCHEMA": "data",
        }
        create_provider.return_value = provider

        parameters = Config.get_db_parameters()

        create_provider.assert_called_once_with()
        provider.get_secret.assert_called_once_with("app-credentials")
        self.assertEqual("database", parameters["db"])
        self.assertEqual("password", parameters["pass"])

    def test_decode_secret_accepts_json_string_and_bytes(self):
        self.assertEqual({"KEY": "value"}, _decode_secret('{"KEY": "value"}', "credentials"))
        self.assertEqual({"KEY": "value"}, _decode_secret(b'{"KEY": "value"}', "credentials"))

    def test_decode_secret_rejects_invalid_json(self):
        with self.assertRaisesRegex(ValueError, "credentials.*valid JSON"):
            _decode_secret("not-json", "credentials")

    def test_decode_secret_rejects_non_json_payload(self):
        with self.assertRaisesRegex(ValueError, "credentials.*valid JSON"):
            _decode_secret(None, "credentials")

    def test_decode_secret_rejects_non_object_json(self):
        with self.assertRaisesRegex(ValueError, "credentials.*JSON object"):
            _decode_secret("[\"value\"]", "credentials")

    def test_decode_secret_rejects_non_string_values(self):
        with self.assertRaisesRegex(ValueError, "string keys and values"):
            _decode_secret('{"KEY": 1}', "credentials")

    def test_secret_store_skips_empty_names_and_merges_secrets(self):
        provider = mock.Mock()
        provider.get_secret.side_effect = [
            {"FIRST": "one"},
            {"SECOND": "two", "FIRST": "updated"},
        ]

        store = SecretStore(provider, ["first-secret", "", "second-secret"])

        self.assertEqual("updated", store.get("FIRST"))
        self.assertEqual("two", store.get("SECOND"))
        self.assertTrue(store.contains("FIRST"))
        self.assertFalse(store.contains("MISSING"))
        provider.get_secret.assert_has_calls([mock.call("first-secret"), mock.call("second-secret")])

    def test_secret_store_raises_for_missing_secret(self):
        store = SecretStore(mock.Mock(), [])

        with self.assertRaises(KeyError):
            store.get("MISSING")

    def test_secret_store_propagates_provider_errors(self):
        provider = mock.Mock()
        provider.get_secret.side_effect = ValueError("provider failed")

        with self.assertRaisesRegex(ValueError, "provider failed"):
            SecretStore(provider, ["credentials"])
