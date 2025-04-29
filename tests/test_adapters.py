import pytest
import logging
from unittest.mock import patch, MagicMock

from slack_sdk.errors import SlackApiError

from app.adapters.email import EmailNotificationAdapter
from app.adapters.slack import SlackNotificationAdapter


def test_email_adapter_send_logs_correctly(caplog):
    """Verify the mock email adapter logs the expected output."""
    caplog.set_level(logging.INFO, logger="app.adapters.email")
    adapter = EmailNotificationAdapter()
    topic = "pricing"
    message = "Test email body"

    adapter.send(topic=topic, message=message)

    assert "[Mock Email] To: pricing_channel@example.com" in caplog.text
    assert "[Mock Email] Subject: New Request - Topic: pricing" in caplog.text
    assert "[Mock Email] Body: Test email body" in caplog.text


@pytest.fixture
def mock_slack_web_client():
    with patch("app.adapters.slack.WebClient") as mock_client_class:
        mock_instance = MagicMock()
        mock_client_class.return_value = mock_instance
        yield mock_instance


def test_slack_adapter_init_success():
    """Verify successful initialization with valid token and channel ID."""
    adapter = SlackNotificationAdapter(token="xoxb-test-token", channel_id="C12345")
    assert adapter.channel_id == "C12345"
    assert adapter.client is not None


def test_slack_adapter_init_raises_value_error_on_missing_token():
    """Verify ValueError is raised if token is missing."""
    with pytest.raises(ValueError, match="Slack token cannot be empty."):
        SlackNotificationAdapter(token="", channel_id="C12345")


def test_slack_adapter_init_raises_value_error_on_missing_channel_id():
    """Verify ValueError is raised if channel ID is missing."""
    with pytest.raises(ValueError, match="Slack channel ID cannot be empty."):
        SlackNotificationAdapter(token="xoxb-test-token", channel_id="")


def test_slack_adapter_send_success(mock_slack_web_client):
    """Verify send calls chat_postMessage with correct arguments."""
    adapter = SlackNotificationAdapter(token="xoxb-test-token", channel_id="C12345")
    topic = "sales"
    message = "Test Slack message"

    adapter.send(topic=topic, message=message)

    expected_text = "*New Assistance Request - Topic: sales*\n> Test Slack message"
    mock_slack_web_client.chat_postMessage.assert_called_once_with(
        channel="C12345", text=expected_text, mrkdwn=True
    )


def test_slack_adapter_send_raises_slack_api_error(mock_slack_web_client, caplog):
    """Verify SlackApiError is logged and raised on API failure."""
    # Simulate a SlackApiError
    mock_response = MagicMock()
    mock_response.__getitem__.side_effect = lambda key: (
        "invalid_auth" if key == "error" else None
    )
    api_error = SlackApiError("API call failed", response=mock_response)
    mock_slack_web_client.chat_postMessage.side_effect = api_error

    adapter = SlackNotificationAdapter(token="xoxb-test-token", channel_id="C12345")
    topic = "sales"
    message = "Test failure message"

    with pytest.raises(SlackApiError):
        adapter.send(topic=topic, message=message)

    assert "Error sending message to Slack channel C12345: invalid_auth" in caplog.text


def test_slack_adapter_send_raises_unexpected_error(mock_slack_web_client, caplog):
    """Verify unexpected errors during send are logged and raised."""
    mock_slack_web_client.chat_postMessage.side_effect = Exception("Network error")

    adapter = SlackNotificationAdapter(token="xoxb-test-token", channel_id="C12345")
    topic = "sales"
    message = "Test unexpected error"

    with pytest.raises(Exception, match="Network error"):
        adapter.send(topic=topic, message=message)

    assert (
        "An unexpected error occurred when sending to Slack: Network error"
        in caplog.text
    )
