"""
Data api wrapped under flask
"""
import logging
import time
import uuid

from flask import Flask, g, request

from src.app_check import PING_BLUEPRINT
from src.caching import Caching
from src.device.controller import DEVICE_BLUEPRINT
from src.image.controller import IMAGE_BLUEPRINT
from src.logger import LoggerAPI
from src.login.controller import LOGIN_BLUEPRINT
from src.search.controller import SEARCH_BLUEPRINT
from src.user.controller import USER_BLUEPRINT


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

        self._app.before_request(assign_request_id)  # pragma: no cover

        Caching.init_cache(self._app)  # pragma: no cover

        from src.migrate_db import run_migrate  # pragma: no cover  # pylint: disable=import-outside-toplevel
        run_migrate()  # pragma: no cover

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
