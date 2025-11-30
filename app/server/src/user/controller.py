"""
User Controller
"""
from flask import Blueprint, Response

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


@USER_BLUEPRINT.route("/done_onboarding", methods=["POST"])
@validate()
def set_user_onboarding_done(user_id: str | None) -> Response:
    """
    :return:
    :rtype:
    """
    data = UserServices().done_user_onboarding(user_id)
    return ValidResponse(
        domain="Done user onboarding",
        detail=user_id,
        data=data
    ).get_response_json()
