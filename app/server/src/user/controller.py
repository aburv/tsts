"""
User Controller
"""
from flask import Blueprint, Response

from src.auth import client_auth
from src.responses import ValidResponse, APIException
from src.user.service import UserServices

USER_BLUEPRINT = Blueprint('user', __name__)


@USER_BLUEPRINT.route("/app", methods=["GET"])
@client_auth
def get_user_data() -> Response:
    """
    :return:
    :rtype:
    """
    try:
        user_id = ""
        data = UserServices().get_user_data(user_id)
        return ValidResponse(
            domain="Retrieved user data",
            detail=user_id,
            content=data
        ).get_response_json()
    except APIException as e:
        return e.get_response_json()
