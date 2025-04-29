import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from app.ports.notification import NotificationChannel

logger = logging.getLogger(__name__)


class SlackNotificationAdapter(NotificationChannel):
    """Sends notifications to a specified Slack channel."""

    def __init__(self, token: str, channel_id: str):
        """Initializes the adapter with Slack token and channel ID.

        Args:
            token: The Slack Bot token.
            channel_id: The ID of the target Slack channel.
        """
        if not token:
            raise ValueError("Slack token cannot be empty.")
        if not channel_id:
            raise ValueError("Slack channel ID cannot be empty.")

        self.client = WebClient(token=token)
        self.channel_id = channel_id
        logger.info(f"SlackNotificationAdapter initialized for channel {channel_id}")

    def send(self, topic: str, message: str) -> None:
        """Sends a message to the configured Slack channel."""
        try:
            text = f"*New Assistance Request - Topic: {topic}*\n> {message}"
            response = self.client.chat_postMessage(
                channel=self.channel_id, text=text, mrkdwn=True
            )
            logger.info(f"Message sent to Slack channel {self.channel_id}")
        except SlackApiError as e:
            logger.error(
                f"Error sending message to Slack channel {self.channel_id}: {e.response['error']}",
                exc_info=True,
            )
            raise
        except Exception as e:
            logger.error(
                f"An unexpected error occurred when sending to Slack: {e}",
                exc_info=True,
            )
            raise
