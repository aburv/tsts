"""
Player Controller
"""

from flask import Blueprint, Response, request

from src.auth import validate
from src.caching import get_if_cached
from src.option.data import FormType
from src.option.service import OptionService
from src.player.service import PlayerServices
from src.player_gear.service import PlayerGearServices
from src.player_position.service import PlayerPositionServices
from src.responses import ValidResponse, APIException, DataValidationException, APIResponse, RuntimeException, \
    RecordNotFoundException
from src.user.service import UserServices

PLAYER_BLUEPRINT = Blueprint('player', __name__)


@PLAYER_BLUEPRINT.route("/form_data", methods=["GET"])
@validate(is_auth_mandatory=False)
@get_if_cached("form_player", user_specific=False, needs_user=True)
def get_option_data(user_id: str | None) -> APIResponse:  # pylint: disable=unused-argument
    """
    :return:
    :rtype:
    """
    data = OptionService(FormType.PLAYER).get_options()
    return ValidResponse(
        "Retrieved option data",
        data
    )


@PLAYER_BLUEPRINT.route("/actual/1", methods=["GET"])
@validate()
def get_actual_1(user_id: str | None) -> Response:
    """
    :return:
    :rtype:
    """
    try:
        player_id = UserServices().get_player_id(user_id)
        data = {}
        if player_id is not None:
            data = PlayerServices().get_user_data(player_id, user_id)
        return ValidResponse(
            "Retrieved player user data",
            data
        ).get_response_json()
    except APIException as e:
        return e.get_response_json()


@PLAYER_BLUEPRINT.route("/actual/2", methods=["GET"])
@validate()
def get_actual_2(user_id: str | None) -> Response:
    """
    :return:
    :rtype:
    """
    try:
        player_id = UserServices().get_player_id(user_id)
        data = {}
        if player_id is not None:
            data = PlayerGearServices().get_by_id(player_id)
        return ValidResponse(
            "Retrieved player user data",
            data
        ).get_response_json()
    except APIException as e:
        return e.get_response_json()


@PLAYER_BLUEPRINT.route("/", methods=["POST"])
@validate()
def create_player(user_id: str | None) -> Response:
    """
    :return:
    :rtype:
    """
    data = request.json.get("data", None)
    try:
        if data is None:
            raise DataValidationException(f"Create or update player User {data}", "No data")
        player_id = UserServices().get_player_id(user_id)
        if player_id is not None:
            PlayerServices().update(player_id, data, user_id)
            return ValidResponse(
                "Updated player with details data",
                True
            ).get_response_json()
        return ValidResponse(
            "Created player with basic details data",
            PlayerServices().create(data, user_id)
        ).get_response_json()
    except APIException as e:
        return e.get_response_json()


@PLAYER_BLUEPRINT.route("/jersey_details", methods=["POST"])
@validate()
def update_player_jersey_details(user_id: str | None) -> Response:
    """
    :return:
    :rtype:
    """
    data = request.json.get("data", None)
    try:
        if data is None:
            raise DataValidationException(f"Create player measurements {data}", "No data")
        player_id = UserServices().get_player_id(user_id)
        if player_id is not None:
            service = PlayerGearServices()
            is_exist = service.check_presence(player_id)
            if not is_exist:
                service.create(player_id, data, user_id)
                msg = "Created player with basic details data"
            else:
                service.update(player_id, data, user_id)
                msg = "Updated player with basic details data"
            try:
                positions = data.get("positions", None)
                if positions is not None and len(positions) > 0:
                    pp_service = PlayerPositionServices()
                    for position in positions:
                        pp_service.create_position(player_id, position, user_id)
            except Exception as e:
                raise RuntimeException(
                    "Unable to create positions",
                    f"{data} on {player_id} {e}"
                ) from e
            return ValidResponse(
                msg,
                True
            ).get_response_json()
        raise RecordNotFoundException("Player for user", user_id)
    except APIException as e:
        return e.get_response_json()


@PLAYER_BLUEPRINT.route("/<r_id>", methods=["GET"])
@validate(is_auth_mandatory=False)
@get_if_cached("player_info", user_specific=False, needs_user=False)
def get_player(r_id: str, user_id: str | None) -> APIResponse:  # pylint: disable=unused-argument
    """
    :return:
    :rtype:
    """
    data = PlayerServices().get_player_info(r_id)
    return ValidResponse(
        "Retrieved player data",
        data
    )
