"""
Image Controller
"""

from flask import Blueprint, Response, request

from src.auth import validate
from src.caching import get_if_cached
from src.image.service import ImageServices
from src.responses import ValidResponse, APIException

IMAGE_BLUEPRINT = Blueprint('image', __name__)

IMAGE_TAG = "image"


@IMAGE_BLUEPRINT.route("/add", methods=["POST"])
@validate(resource=IMAGE_TAG, permission="create")
def add_image(user_id: str | None) -> Response:
    """
    :return:
    :rtype:
    """
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


@IMAGE_BLUEPRINT.route("/<r_id>/<size>", methods=["GET"])
@validate(is_required=False)
@get_if_cached(api_key="image")
def get_image(r_id, size) -> bytes:
    """
    :return:
    :rtype:
    """
    try:
        image_data = ImageServices().get(r_id, size)
        return image_data
    except APIException as _:
        return b''


@IMAGE_BLUEPRINT.route("/<r_id>/", methods=["GET"])
@validate(resource=IMAGE_TAG, permission="view")
@get_if_cached(api_key="image")
def get_original_image(r_id, user_id: str | None) -> bytes:
    """
    :return:
    :rtype:
    """
    try:
        image_data = ImageServices().get(r_id, None)
        return image_data
    except APIException as _:
        return b''
