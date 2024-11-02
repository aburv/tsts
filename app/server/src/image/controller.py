"""
Image Controller
"""

from flask import Blueprint, Response, request

from src.auth import client_auth
# from src.caching import cache, Config
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
        # print(file)
        # print(file.headers)
        # print(file.filename)
        # print(file.name)
        # print(file.mimetype_params)
        # print(file.content_type)
        # print(file.content_length)
        image = ImageServices().add(file, user_id)
        return ValidResponse(
            domain="New image",
            detail=str(file.filename),
            content=image
        ).get_response_json()
    except APIException as e:
        return e.get_response_json()


@IMAGE_BLUEPRINT.route("/<i_id>/<size>", methods=["GET"])
# @cache.cached()
@client_auth
def get_image(i_id, size) -> Response:
    """
    :return:
    :rtype:
    """
    # cache.delete(f'{Config.CACHE_KEY_PREFIX}:data/{i_id}')
    try:
        image_data = ImageServices().get(i_id, size)
        return Response(image_data, mimetype='image/png')
    except APIException as _:
        return Response(b'', mimetype='image/png')


@IMAGE_BLUEPRINT.route("/<i_id>/", methods=["GET"])
# @cache.cached()
@client_auth
def get_original_image(i_id) -> Response:
    """
    :return:
    :rtype:
    """
    # cache.delete(f'{Config.CACHE_KEY_PREFIX}:data/{i_id}')
    try:
        image_data = ImageServices().get(i_id, None)
        return Response(image_data, mimetype='image/png')
    except APIException as _:
        return Response(b'', mimetype='image/png')
