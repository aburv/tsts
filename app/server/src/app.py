"""
Data api wrapped under flask
"""
from flask import Flask
from flask_cors import CORS

from src.app_check import PING_BLUEPRINT
from src.device.controller import DEVICE_BLUEPRINT
from src.user.controller import USER_BLUEPRINT

APP = Flask(__name__)

cors = CORS(APP,
            resources={
                r"/api/*": {
                    "origins": "*"
                }
            })

APP.register_blueprint(PING_BLUEPRINT, url_prefix="/api/ping")

APP.register_blueprint(USER_BLUEPRINT, url_prefix="/api/user")
APP.register_blueprint(DEVICE_BLUEPRINT, url_prefix="/api/device")
