"""
User Controller
"""
from flask import Blueprint, Response, request

from src.auth import validate
from src.caching import get_if_cached
from src.responses import APIException, ValidResponse, APIResponse
from src.user.service import UserServices

from src.image.service import ImageServices


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


@USER_BLUEPRINT.route("/image", methods=["POST"])
@validate()
def update_image(user_id: str | None) -> Response:
    """
    :return:
    :rtype:
    """
    try:
        file = request.files['file']
        image_id = ImageServices().add(file, user_id)
        UserServices().update_image(image_id, user_id)
        return ValidResponse(
            domain="Updated the image",
            detail=user_id,
            data=image_id
        ).get_response_json()
    except Exception as err:
        APIException("Update the image", str(err), "", "", is_error=False)
        return ValidResponse(
            domain="Update the image",
            detail=user_id,
            data=""
        ).get_response_json()
