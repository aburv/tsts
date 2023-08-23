"""
Data api wrapped under flask
"""
from flask import Flask
from flask_cors import CORS

APP = Flask(__name__)

cors = CORS(APP,
            resources={
                r"/api/*": {
                    "origins": "*"
                }
            })

# if __name__ == '__main__':
#     APP.run(host="0.0.0.0", port=9000)
