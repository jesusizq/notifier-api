import pytest
from unittest.mock import patch

from app import create_app
from app.domain.models import AssistanceRequest


@pytest.fixture(scope="module")
def app():
    from config import config

    # Assuming config['testing'] provides all necessary configurations
    # including valid SLACK_BOT_TOKEN and SLACK_CHANNEL_ID
    flask_app = create_app(config["testing"])
    yield flask_app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_health_check(client):
    response = client.get("/v1/health/")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


@patch("app.use_cases.handle_request.HandleAssistanceRequest.execute")
def test_notify_sales_success(mock_execute, client):
    data = {"topic": "sales", "description": "Help with sales inquiry"}
    response = client.post("/v1/notify/", json=data)

    assert response.status_code == 202
    assert response.json == {"message": "Request received and processing."}

    mock_execute.assert_called_once()
    call_args, _ = mock_execute.call_args
    assert isinstance(call_args[0], AssistanceRequest)
    assert call_args[0].topic == "sales"
    assert call_args[0].description == "Help with sales inquiry"


@patch("app.use_cases.handle_request.HandleAssistanceRequest.execute")
def test_notify_pricing_success(mock_execute, client):
    data = {"topic": "pricing", "description": "Help with pricing question"}
    response = client.post("/v1/notify/", json=data)

    assert response.status_code == 202
    assert response.json == {"message": "Request received and processing."}
    mock_execute.assert_called_once()
    call_args, _ = mock_execute.call_args
    assert isinstance(call_args[0], AssistanceRequest)
    assert call_args[0].topic == "pricing"
    assert call_args[0].description == "Help with pricing question"


@patch("app.use_cases.handle_request.HandleAssistanceRequest.execute")
def test_notify_unknown_topic_success(mock_execute, client):
    data = {"topic": "sales", "description": "Help with technical issue"}
    response = client.post("/v1/notify/", json=data)

    assert response.status_code == 202
    assert response.json == {"message": "Request received and processing."}
    mock_execute.assert_called_once()
    call_args, _ = mock_execute.call_args
    assert call_args[0].topic == "sales"
    assert call_args[0].description == "Help with technical issue"


@patch("app.use_cases.handle_request.HandleAssistanceRequest.execute")
def test_notify_missing_topic_fails(mock_execute, client):
    data = {"description": "Missing topic field"}
    response = client.post("/v1/notify/", json=data)
    assert response.status_code == 400
    assert "Topic is required." in response.json["messages"]["json"]["topic"][0]
    mock_execute.assert_not_called()


@patch("app.use_cases.handle_request.HandleAssistanceRequest.execute")
def test_notify_missing_description_fails(mock_execute, client):
    data = {"topic": "sales"}
    response = client.post("/v1/notify/", json=data)

    assert response.status_code == 400
    assert (
        "Description is required."
        in response.json["messages"]["json"]["description"][0]
    )
    mock_execute.assert_not_called()


@patch("app.use_cases.handle_request.HandleAssistanceRequest.execute")
def test_notify_extra_field_ignored(mock_execute, client):
    data = {"topic": "sales", "description": "Extra field test", "extra": "value"}
    response = client.post("/v1/notify/", json=data)

    assert response.status_code == 400


@patch("app.use_cases.handle_request.HandleAssistanceRequest.execute")
def test_notify_wrong_content_type_fails(mock_execute, client):
    data = "<xml>data</xml>"
    response = client.post("/v1/notify/", data=data, content_type="application/xml")

    assert response.status_code == 400
    mock_execute.assert_not_called()
