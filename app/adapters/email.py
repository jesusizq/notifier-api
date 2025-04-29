import logging

from app.ports.notification import NotificationChannel

logger = logging.getLogger(__name__)


class EmailNotificationAdapter(NotificationChannel):
    """A notification channel that sends emails (mocked)."""

    def send(self, topic: str, message: str) -> None:
        """Logs the notification message instead of sending an email."""
        logger.info(f"[Mock Email] To: {topic}_channel@example.com")
        logger.info(f"[Mock Email] Subject: New Request - Topic: {topic}")
        logger.info(f"[Mock Email] Body: {message}")
