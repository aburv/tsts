"""
Search Controller
"""
from flask import Blueprint

from src.auth import validate
from src.caching import get_if_cached
from src.responses import ValidResponse, APIResponse
from src.search.service import SearchServices

SEARCH_BLUEPRINT = Blueprint('search', __name__)


@SEARCH_BLUEPRINT.route("/<text>", methods=["GET"])
@validate(is_auth_mandatory=False)
@get_if_cached(api_key="search")
def get_data(text: str, user_id: str | None) -> APIResponse:
    """
    :return:
    :rtype:
    """
    data = SearchServices().search(text, user_id)
    return ValidResponse(
        domain="Search Results",
        detail=text,
        data=data
    )
