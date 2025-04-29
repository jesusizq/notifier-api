import pytest
import logging
from unittest.mock import Mock

from app.domain.models import AssistanceRequest
from app.use_cases.handle_request import HandleAssistanceRequest
from app.ports.notification import NotificationChannel


@pytest.fixture
def mock_sales_channel():
    return Mock(spec=NotificationChannel)


@pytest.fixture
def mock_pricing_channel():
    return Mock(spec=NotificationChannel)


@pytest.fixture
def handler(mock_sales_channel, mock_pricing_channel):
    channels = {
        "sales": mock_sales_channel,
        "pricing": mock_pricing_channel,
    }
    return HandleAssistanceRequest(channels=channels)


def test_handle_sales_request_routes_to_sales_channel(
    handler, mock_sales_channel, mock_pricing_channel
):
    """Verify sales requests are sent to the sales channel."""
    request = AssistanceRequest(topic="sales", description="Need help with sales")
    handler.execute(request)

    mock_sales_channel.send.assert_called_once_with(
        topic="sales", message="Need help with sales"
    )
    mock_pricing_channel.send.assert_not_called()


def test_handle_pricing_request_routes_to_pricing_channel(
    handler, mock_sales_channel, mock_pricing_channel
):
    """Verify pricing requests are sent to the pricing channel."""
    request = AssistanceRequest(topic="pricing", description="Need help with pricing")
    handler.execute(request)

    mock_pricing_channel.send.assert_called_once_with(
        topic="pricing", message="Need help with pricing"
    )
    mock_sales_channel.send.assert_not_called()


def test_handle_unknown_topic_does_not_send(
    handler, mock_sales_channel, mock_pricing_channel
):
    """Verify requests with unknown topics are not sent anywhere."""
    request = AssistanceRequest(topic="support", description="Need help with support")
    handler.execute(request)

    mock_sales_channel.send.assert_not_called()
    mock_pricing_channel.send.assert_not_called()


def test_handle_request_logs_warning_for_unknown_topic(handler, caplog):
    """Verify a warning is logged for unknown topics."""
    request = AssistanceRequest(topic="support", description="Need help with support")
    handler.execute(request)

    assert "No notification channel configured for topic: support" in caplog.text


def test_handle_request_logs_info_on_successful_send(
    handler, mock_sales_channel, caplog
):
    """Verify info is logged on successful send."""
    caplog.set_level(logging.INFO, logger="app.use_cases.handle_request")
    request = AssistanceRequest(topic="sales", description="Info log test")
    handler.execute(request)
    mock_sales_channel.send.assert_called_once_with(
        topic="sales", message="Info log test"
    )
    assert "Sent notification for topic 'sales'" in caplog.text
    assert "Mock" in caplog.text  # Checks if the type name is logged


def test_handle_request_logs_error_on_send_failure(handler, mock_sales_channel, caplog):
    """Verify error is logged if channel send fails."""
    caplog.set_level(logging.ERROR, logger="app.use_cases.handle_request")
    mock_sales_channel.send.side_effect = Exception("Slack API error")
    request = AssistanceRequest(topic="sales", description="Error log test")
    handler.execute(request)

    assert "Failed to send notification for topic 'sales'" in caplog.text
    assert "Slack API error" in caplog.text
