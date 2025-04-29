from dataclasses import dataclass


@dataclass(frozen=True)
class AssistanceRequest:
    """Represents a customer assistance request."""

    topic: str
    description: str
