from abc import ABC, abstractmethod
from app.domain.models import AssistanceRequest


class HandleAssistanceRequestBase(ABC):
    """Interface for the use case handling assistance requests."""

    @abstractmethod
    def execute(self, request: AssistanceRequest) -> None:
        """Processes the assistance request and routes it."""
        pass
