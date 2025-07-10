"""
Device Controller
"""

from flask import Blueprint, Response, request

from src.auth import validate
from src.device.service import DeviceServices
from src.responses import ValidResponse, APIException

DEVICE_BLUEPRINT = Blueprint('device', __name__)


@DEVICE_BLUEPRINT.route("/register", methods=["POST"])
@validate(is_required=False)
def set_device_data() -> Response:
    """
    :return:
    :rtype:
    """
    data = request.json.get("data", {})
    try:
        device = DeviceServices().register_device(data)
        return ValidResponse(
            domain="New Device",
            detail=data,
            data=device
        ).get_response_json()
    except APIException as e:
        return e.get_response_json()
