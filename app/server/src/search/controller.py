"""
User Controller
"""
from flask import Blueprint

from src.auth import client_auth
from src.caching import get_if_cached
from src.responses import ValidResponse, APIResponse
from src.search.service import SearchServices

SEARCH_BLUEPRINT = Blueprint('search', __name__)


@SEARCH_BLUEPRINT.route("/<text>", methods=["GET"])
@client_auth
@get_if_cached(api_key="search")
def get_data(text) -> APIResponse:
    """
    :return:
    :rtype:
    """
    data = SearchServices().search(text)
    return ValidResponse(
        domain="Search Results",
        detail=text,
        data=data
    )
