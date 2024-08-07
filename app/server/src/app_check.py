"""
Ping Controller
"""
from flask import Blueprint, Response, make_response

from src.auth import client_auth

PING_BLUEPRINT = Blueprint('ping', __name__)


@PING_BLUEPRINT.route("/", methods=["POST"])
@client_auth
def ping() -> Response:
    """
    :return:
    :rtype:
    """
    return make_response({'data': 'success'}, 200)


@PING_BLUEPRINT.route("/aws", methods=["GET"])
def ping_aws() -> Response:
    """
    :return:
    :rtype:
    """
    return make_response({'data': 'success'}, 200)
