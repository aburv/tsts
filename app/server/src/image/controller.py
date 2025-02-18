"""
Image Controller
"""

from flask import Blueprint, Response, request

from src.auth import client_auth
from src.caching import get_if_cached
from src.image.service import ImageServices
from src.responses import ValidResponse, APIException

IMAGE_BLUEPRINT = Blueprint('image', __name__)


@IMAGE_BLUEPRINT.route("/add", methods=["POST"])
@client_auth
def add_image() -> Response:
    """
    :return:
    :rtype:
    """
    user_id = ""
    try:
        file = request.files['file']
        image = ImageServices().add(file, user_id)
        return ValidResponse(
            domain="New Image",
            detail=str(file.filename),
            data=image
        ).get_response_json()
    except APIException as e:
        return e.get_response_json()


@IMAGE_BLUEPRINT.route("/<i_id>/<size>", methods=["GET"])
@client_auth
@get_if_cached(api_key="image")
def get_image(i_id, size) -> bytes:
    """
    :return:
    :rtype:
    """
    try:
        image_data = ImageServices().get(i_id, size)
        return image_data
    except APIException as _:
        return b''


@IMAGE_BLUEPRINT.route("/<i_id>/", methods=["GET"])
@client_auth
@get_if_cached(api_key="image")
def get_original_image(i_id) -> bytes:
    """
    :return:
    :rtype:
    """
    try:
        image_data = ImageServices().get(i_id, None)
        return image_data
    except APIException as _:
        return b''
