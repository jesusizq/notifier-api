import logging
from flask import current_app, make_response, jsonify, request
from apifairy import arguments, response
from typing import cast

from ..domain.models import AssistanceRequest
from ..use_cases.handle_request import HandleAssistanceRequest
from .schemas.schemas import AssistanceRequestSchema, NotificationResponseSchema
from . import notify_bp

logger = logging.getLogger(__name__)


@notify_bp.route("", methods=["POST"], strict_slashes=False)
@arguments(AssistanceRequestSchema, location="json")
@response(NotificationResponseSchema, status_code=202)
def handle_notification(validated_data):
    """Handle incoming assistance requests."""

    try:
        assistance_request = AssistanceRequest(
            topic=validated_data["topic"],
            description=validated_data["description"],
        )

        logger.info(
            f"Received assistance request: topic='{assistance_request.topic}', "
            f"description='{assistance_request.description[:50]}...'"
        )

        handler = cast(HandleAssistanceRequest, current_app.assistance_request_handler)
        handler.execute(assistance_request)

        logger.info(
            f"Assistance request for topic '{assistance_request.topic}' processed."
        )

        return {"message": "Request received and processing."}

    except Exception as e:
        logger.error(f"Error handling notification: {e}", exc_info=True)
        return make_response(
            jsonify({"error": "An internal server error occurred"}), 500
        )
