from abc import ABC, abstractmethod


class NotificationChannel(ABC):
    """Interface for sending notifications to different channels."""

    @abstractmethod
    def send(self, topic: str, message: str) -> None:
        """Sends a message related to a specific topic."""
        pass
