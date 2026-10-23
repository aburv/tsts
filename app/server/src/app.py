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
from src.client.controller import CLIENT_BLUEPRINT
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
    g.start_time = time.perf_counter()
    request_id = str(uuid.uuid4())
    g.request_id = request_id

    LoggerAPI().info_entry(
        f"{g.request_id} - {request.remote_addr} - {request.method} {request.path}"
    )


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
        self._app.logger.propagate = False

        logging.getLogger('flask').setLevel(logging.ERROR)
        logging.getLogger('werkzeug').setLevel(logging.ERROR)

        LoggerAPI().info_entry("Logger initialized and setting request id before all request")

        self._app.before_request(assign_request_id)

        LoggerAPI().info_entry("Secret store are setting")

        provider = Config.create_secret_provider()
        secret_names = [name.strip()
                        for name in os.getenv("SECRET_NAMES", "").split(",")
                        if name.strip()]
        if not secret_names:
            if os.getenv("SECRET_PROVIDER", "").strip().lower() != "env":
                raise ValueError("SECRET_NAMES must list the configured JSON secrets")
            secret_names = list(SECRET_KEYS)
        secret_store = SecretStore(provider, secret_names=secret_names)
        Config.set_secret_store(secret_store)
        Config.validate_secret_store()
        self._app.config["SECRET_STORE"] = secret_store

        LoggerAPI().info_entry("Initializing cache")

        Caching.init_cache(self._app)

    def _set_routes(self):
        """
        Setup routes
        """
        self._app.register_blueprint(PING_BLUEPRINT, url_prefix="/api/ping")
        self._app.register_blueprint(CLIENT_BLUEPRINT, url_prefix="/api/client")

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
        self._set_up()

        self._set_routes()

    def get_app(self):
        """
        Get app instance
        """
        return self._app
