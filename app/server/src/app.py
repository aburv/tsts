"""
Data api wrapped under flask
"""
from flask import Flask
from flask_cors import CORS

from src.app_check import PING_BLUEPRINT
from src.caching import Caching
from src.device.controller import DEVICE_BLUEPRINT
from src.image.controller import IMAGE_BLUEPRINT
from src.search.controller import SEARCH_BLUEPRINT
from src.user.controller import USER_BLUEPRINT


class App:
    """
    API App
    """

    @staticmethod
    def create():
        """
        Configuring app with cors, blueprints and cache
        """
        app = Flask(__name__)

        CORS(app,
             resources={
                 r"/api/*": {
                     "origins": "*"
                 }
             })

        Caching.init_cache(app)

        app.register_blueprint(PING_BLUEPRINT, url_prefix="/api/ping")

        app.register_blueprint(USER_BLUEPRINT, url_prefix="/api/user")
        app.register_blueprint(DEVICE_BLUEPRINT, url_prefix="/api/device")

        app.register_blueprint(IMAGE_BLUEPRINT, url_prefix="/api/image")

        app.register_blueprint(SEARCH_BLUEPRINT, url_prefix="/api/search")

        return app
