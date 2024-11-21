"""
User Controller
"""
from flask import Blueprint, Response

from src.auth import client_auth
from src.responses import ValidResponse, APIException
from src.search.service import SearchServices

SEARCH_BLUEPRINT = Blueprint('search', __name__)


@SEARCH_BLUEPRINT.route("/<text>", methods=["GET"])
@client_auth
def get_data(text) -> Response:
    """
    :return:
    :rtype:
    """
    try:
        data = SearchServices().search(text)
        return ValidResponse(
            domain="Search Results",
            detail=text,
            content=data
        ).get_response_json()
    except APIException as e:
        return e.get_response_json()
