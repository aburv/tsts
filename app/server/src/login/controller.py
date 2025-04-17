"""
User Controller
"""
from flask import Blueprint, Response, request

from src.auth import validate
from src.login.service import LoginServices
from src.responses import ValidResponse, DataValidationException, APIException

LOGIN_BLUEPRINT = Blueprint('login', __name__)


@LOGIN_BLUEPRINT.route("/login", methods=["POST"])
@validate(is_required=False)
def get_user_token() -> Response:
    """
    :return:
    :rtype:
    """
    data = request.json.get("data", None)
    try:
        if data is None:
            raise DataValidationException("Login", "No Data")
        user_data = data.get("user", None)
        login_data = data.get("login", None)
        if user_data is None:
            raise DataValidationException(f"Login {user_data} {login_data}", "No user Data")
        if login_data is None:
            raise DataValidationException(f"Login {user_data} {login_data}", "No login Data")
        login_data.update({"ip": request.remote_addr})
        return ValidResponse(
            domain="Get user token",
            data=LoginServices().login(user_data, login_data),
            detail=f"{user_data} {login_data}"
        ).get_response_json()
    except APIException as e:
        return e.get_response_json()


@LOGIN_BLUEPRINT.route("/refresh_token", methods=["GET"])
@validate(is_required=False)
def refresh_user_access_token() -> Response:
    """
    :return:
    :rtype:
    """
    token = request.headers.get("x-access-key", "")
    try:
        return ValidResponse(
            domain="Get updated user access token",
            data=LoginServices.refresh(token),
            detail=f"{token}"
        ).get_response_json()
    except APIException as e:
        return e.get_response_json()
