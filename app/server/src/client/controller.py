"""Client installation bootstrap endpoints."""
import base64
import re

from flask import Blueprint, request

from src.client.service import ClientSessionService
from src.responses import APIException, DataValidationException, ValidResponse


CLIENT_BLUEPRINT = Blueprint("client", __name__)
_INSTALLATION_ID = re.compile(r"^[A-Za-z0-9_-]{16,128}$")
_PLATFORMS = {"android", "ios", "web"}


@CLIENT_BLUEPRINT.route("/challenge", methods=["POST"])
def challenge():
    """
    Challenge endpoint
    """
    try:
        body = request.get_json(silent=True) or {}
        data = body.get("data", body)
        installation_id = data.get("installationId", "")
        public_key = data.get("publicKey", "")
        platform = data.get("platform", "")
        if not _INSTALLATION_ID.fullmatch(installation_id):
            raise DataValidationException("Installation", "Invalid installation ID")
        if platform not in _PLATFORMS:
            raise DataValidationException("Platform", "Invalid platform")
        try:
            base64.b64decode(public_key, validate=True)
        except (ValueError, TypeError):
            raise DataValidationException("Public key", "Invalid public key") from None
        challenge_value = ClientSessionService.create_challenge(
            installation_id, public_key, platform
        )
        return ValidResponse("Client", {"challenge": challenge_value}).get_response_json()
    except APIException as error:
        return error.get_response_json()


@CLIENT_BLUEPRINT.route("/session", methods=["POST"])
def session():
    """
    Session endpoint
    """
    try:
        body = request.get_json(silent=True) or {}
        data = body.get("data", body)
        installation_id = data.get("installationId", "")
        platform = data.get("platform", "")
        challenge_value = data.get("challenge", "")
        signature = data.get("signature", "")
        if not _INSTALLATION_ID.fullmatch(installation_id):
            raise DataValidationException("Installation", "Invalid installation ID")
        if platform not in _PLATFORMS:
            raise DataValidationException("Platform", "Invalid platform")
        token_data = ClientSessionService.create_from_challenge(
            installation_id, platform, challenge_value, signature
        )
        return ValidResponse("Client", {
            "clientToken": token_data[0],
            "expiresAt": token_data[1],
        }).get_response_json()
    except APIException as error:
        return error.get_response_json()
