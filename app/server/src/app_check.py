"""
Ping Controller
"""
from flask import Blueprint, Response, make_response

from src.auth import validate

PING_BLUEPRINT = Blueprint('ping', __name__)


@PING_BLUEPRINT.route("/", methods=["POST"])
@validate(is_required=False)
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
