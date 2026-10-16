import unittest
from unittest import mock

from src.config import Config, SECRET_KEYS
from src.app import (
    App,
    CLIENT_BLUEPRINT,
    DEVICE_BLUEPRINT,
    IMAGE_BLUEPRINT,
    LOGIN_BLUEPRINT,
    PING_BLUEPRINT,
    PLAYER_BLUEPRINT,
    SEARCH_BLUEPRINT,
    USER_BLUEPRINT,
    assign_request_id,
    g,
)


class AppTest(unittest.TestCase):

    @mock.patch("src.app.LoggerAPI")
    @mock.patch("src.app.uuid.uuid4", return_value="request-id")
    @mock.patch("src.app.time.perf_counter", return_value=12.5)
    def test_assign_request_id_calls_dependencies_with_expected_arguments(
        self,
        perf_counter,
        uuid4,
        logger_api,
    ):
        app = App()

        with app.get_app().test_request_context(
            "/players",
            method="POST",
            environ_base={"REMOTE_ADDR": "127.0.0.1"},
        ):
            assign_request_id()

            self.assertEqual(g.start_time, 12.5)
            self.assertEqual(g.request_id, "request-id")

        perf_counter.assert_called_once_with()
        uuid4.assert_called_once_with()
        logger_api.assert_called_once_with()
        logger_api.return_value.info_entry.assert_called_once_with(
            "request-id - 127.0.0.1 - POST /players"
        )

    def test_get_app_returns_application_instance(self):
        app = App()

        result = app.get_app()

        self.assertIs(result, app._app)

    @mock.patch("src.app.Caching.init_cache")
    @mock.patch("src.app.Config.validate_secret_store")
    @mock.patch("src.app.Config.set_secret_store")
    @mock.patch("src.app.SecretStore")
    @mock.patch("src.app.Config.create_secret_provider")
    @mock.patch("src.app.LoggerAPI")
    def test_set_up_calls_dependencies_with_expected_arguments(
        self,
        logger_api,
        create_secret_provider,
        secret_store,
        set_secret_store,
        validate_secret_store,
        init_cache,
    ):
        app = App()
        provider = object()
        store = object()
        create_secret_provider.return_value = provider
        secret_store.return_value = store

        with mock.patch.dict(
            "os.environ",
            {"SECRET_PROVIDER": "env", "SECRET_NAMES": "first, second"},
        ), mock.patch.object(app.get_app(), "before_request") as before_request:
            app._set_up()

        create_secret_provider.assert_called_once_with()
        secret_store.assert_called_once_with(provider, secret_names=["first", "second"])
        set_secret_store.assert_called_once_with(store)
        validate_secret_store.assert_called_once_with()
        before_request.assert_called_once_with(mock.ANY)
        init_cache.assert_called_once_with(app.get_app())
        logger_api.return_value.info_entry.assert_has_calls([
            mock.call("Logger initialized and setting request id before all request"),
            mock.call("Secret store are setting"),
            mock.call("Initializing cache"),
        ])
        self.assertEqual(logger_api.return_value.info_entry.call_count, 3)

    @mock.patch("src.app.Config.create_secret_provider")
    @mock.patch("src.app.LoggerAPI")
    def test_set_up_without_secret_names_raises_for_non_env_provider(
        self,
        logger_api,
        create_secret_provider,
    ):
        app = App()

        with mock.patch.dict(
            "os.environ",
            {"SECRET_PROVIDER": "json"},
            clear=True,
        ), self.assertRaises(ValueError):
            app._set_up()

        create_secret_provider.assert_called_once_with()

    @mock.patch("src.app.Caching.init_cache")
    @mock.patch("src.app.Config.validate_secret_store")
    @mock.patch("src.app.Config.set_secret_store")
    @mock.patch("src.app.SecretStore")
    @mock.patch("src.app.Config.create_secret_provider")
    @mock.patch("src.app.LoggerAPI")
    def test_set_up_without_secret_names_uses_secret_keys_for_env_provider(
        self,
        logger_api,
        create_secret_provider,
        secret_store,
        set_secret_store,
        validate_secret_store,
        init_cache,
    ):
        app = App()
        provider = object()
        store = object()
        create_secret_provider.return_value = provider
        secret_store.return_value = store

        with mock.patch.dict(
            "os.environ",
            {"SECRET_PROVIDER": "env"},
            clear=True,
        ), mock.patch.object(app.get_app(), "before_request"):
            app._set_up()

        secret_store.assert_called_once_with(provider, secret_names=list(SECRET_KEYS))
        set_secret_store.assert_called_once_with(store)
        validate_secret_store.assert_called_once_with()
        init_cache.assert_called_once_with(app.get_app())

    @mock.patch.object(App, "_set_routes")
    @mock.patch.object(App, "_set_up")
    def test_create_calls_setup_and_routes(self, set_up, set_routes):
        app = App()

        app.create()

        set_up.assert_called_once_with()
        set_routes.assert_called_once_with()

    def test_set_routes_registers_blueprints_with_expected_prefixes(self):
        app = App()

        with mock.patch.object(app.get_app(), "register_blueprint") as register_blueprint:
            app._set_routes()

        register_blueprint.assert_has_calls([
            mock.call(PING_BLUEPRINT, url_prefix="/api/ping"),
            mock.call(CLIENT_BLUEPRINT, url_prefix="/api/client"),
            mock.call(USER_BLUEPRINT, url_prefix="/api/user"),
            mock.call(LOGIN_BLUEPRINT, url_prefix="/api/auth"),
            mock.call(DEVICE_BLUEPRINT, url_prefix="/api/device"),
            mock.call(IMAGE_BLUEPRINT, url_prefix="/api/image"),
            mock.call(SEARCH_BLUEPRINT, url_prefix="/api/search"),
            mock.call(PLAYER_BLUEPRINT, url_prefix="/api/player"),
        ])
        self.assertEqual(register_blueprint.call_count, 8)
