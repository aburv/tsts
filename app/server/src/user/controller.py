"""
User Controller
"""
from flask import Blueprint

from src.auth import validate
from src.caching import get_if_cached
from src.responses import ValidResponse, APIResponse
from src.user.service import UserServices

USER_BLUEPRINT = Blueprint('user', __name__)


@USER_BLUEPRINT.route("/app", methods=["GET"])
@validate(is_auth_mandatory=False)
@get_if_cached("app_user")
def get_user_data(user_id: str | None) -> APIResponse:
    """
    :return:
    :rtype:
    """
    data = UserServices().get_user_data(user_id)
    return ValidResponse(
        domain="Retrieved user data",
        detail=user_id,
        data=data
    )
