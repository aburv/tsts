"""
Data api wrapped under flask
"""
import logging
import os
import time
import uuid

from flask import Flask, g, request

from src.secret_manager import SecretStore
from src.config import Config, SECRET_KEYS
from src.app_check import PING_BLUEPRINT
from src.caching import Caching
from src.device.controller import DEVICE_BLUEPRINT
from src.image.controller import IMAGE_BLUEPRINT
from src.logger import LoggerAPI
from src.login.controller import LOGIN_BLUEPRINT
from src.search.controller import SEARCH_BLUEPRINT
from src.user.controller import USER_BLUEPRINT

from src.player.controller import PLAYER_BLUEPRINT


def assign_request_id():
    """
    Assign request ID
    """
    g.start_time = time.perf_counter()  # pragma: no cover
    request_id = str(uuid.uuid4())  # pragma: no cover
    g.request_id = request_id  # pragma: no cover

    LoggerAPI().info_entry(
        f"{g.request_id} - {request.remote_addr} - {request.method} {request.path}"
    )  # pragma: no cover


class App:
    """
    API App
    """

    def __init__(self):
        self._app = Flask(__name__)

    def _set_up(self):
        """
        Setup App settings
        """
        self._app.logger.propagate = False  # pragma: no cover

        logging.getLogger('flask').setLevel(logging.ERROR)  # pragma: no cover
        logging.getLogger('werkzeug').setLevel(logging.ERROR)  # pragma: no cover

        LoggerAPI().info_entry("Logger initialized and setting request id before all request")  # pragma: no cover

        self._app.before_request(assign_request_id)  # pragma: no cover

        LoggerAPI().info_entry("Secret store are setting")  # pragma: no cover

        provider = Config.create_secret_provider()  # pragma: no cover
        secret_names = [name.strip() for name in os.getenv("SECRET_NAMES", "").split(",") if
                        name.strip()]  # pragma: no cover
        if not secret_names:  # pragma: no cover
            if os.getenv("SECRET_PROVIDER", "").strip().lower() != "env":  # pragma: no cover
                raise ValueError("SECRET_NAMES must list the configured JSON secrets")  # pragma: no cover
            secret_names = list(SECRET_KEYS)  # pragma: no cover
        secret_store = SecretStore(provider, secret_names=secret_names)  # pragma: no cover
        Config.set_secret_store(secret_store)  # pragma: no cover
        Config.validate_secret_store()  # pragma: no cover
        self._app.config["SECRET_STORE"] = secret_store  # pragma: no cover

        LoggerAPI().info_entry("Initializing cache")  # pragma: no cover

        Caching.init_cache(self._app)  # pragma: no cover

    def _set_routes(self):
        """
        Setup routes
        """
        self._app.register_blueprint(PING_BLUEPRINT, url_prefix="/api/ping")

        self._app.register_blueprint(USER_BLUEPRINT, url_prefix="/api/user")
        self._app.register_blueprint(LOGIN_BLUEPRINT, url_prefix="/api/auth")

        self._app.register_blueprint(DEVICE_BLUEPRINT, url_prefix="/api/device")

        self._app.register_blueprint(IMAGE_BLUEPRINT, url_prefix="/api/image")

        self._app.register_blueprint(SEARCH_BLUEPRINT, url_prefix="/api/search")

        self._app.register_blueprint(PLAYER_BLUEPRINT, url_prefix="/api/player")

    def create(self):
        """
        Configuring app with cors, blueprints and cache
        """
        self._set_up()  # pragma: no cover

        self._set_routes()  # pragma: no cover

    def get_app(self):
        """
        Get app instance
        """
        return self._app  # pragma: no cover
