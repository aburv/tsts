"""
User Controller
"""
from flask import Blueprint, Response

from src.auth import client_auth
from src.responses import ValidResponse

USER_BLUEPRINT = Blueprint('user', __name__)


@USER_BLUEPRINT.route("/app", methods=["GET"])
@client_auth
def get_user_data() -> Response:
    """
    :return:
    :rtype:
    """
    return ValidResponse("retrieved user data", {'data': 'success'}).get_response_json()
