import logging
from typing import Dict

from app.domain.models import AssistanceRequest
from app.ports.notification import NotificationChannel
from app.ports.use_cases import HandleAssistanceRequestBase

logger = logging.getLogger(__name__)


class HandleAssistanceRequest(HandleAssistanceRequestBase):
    """Concrete implementation for handling assistance requests."""

    def __init__(self, channels: Dict[str, NotificationChannel]):
        """Initializes the use case with notification channels.

        Args:
            channels: A dictionary mapping topic strings to NotificationChannel instances.
        """
        self.channels = channels

    def execute(self, request: AssistanceRequest) -> None:
        """Routes the request to the appropriate channel based on topic."""
        channel = self.channels.get(request.topic)

        if channel:
            try:
                channel.send(topic=request.topic, message=request.description)
                logger.info(
                    f"Sent notification for topic '{request.topic}' via {type(channel).__name__}"
                )
            except Exception as e:
                logger.error(
                    f"Failed to send notification for topic '{request.topic}' via {type(channel).__name__}: {e}",
                    exc_info=True,
                )
        else:
            logger.warning(
                f"No notification channel configured for topic: {request.topic}"
            )
