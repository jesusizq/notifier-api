import os
import tempfile
import logging
from flask import Flask
from apifairy import APIFairy
from flask_caching import Cache
from flask_marshmallow import Marshmallow
from .adapters.email import EmailNotificationAdapter
from .adapters.slack import SlackNotificationAdapter
from .use_cases.handle_request import HandleAssistanceRequest

apifairy = APIFairy()
ma = Marshmallow()
cache = Cache(
    config={
        "CACHE_TYPE": "FileSystemCache",
        "CACHE_DIR": os.path.join(tempfile.gettempdir(), "cache"),
    }
)


def create_app(config_name):
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s.%(msecs)03d] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    app = Flask(__name__)
    app.config.from_object(config_name)

    logging.getLogger(__name__).info(f"Flask app created with config: {config_name}")

    email_adapter = EmailNotificationAdapter()
    slack_token = app.config.get("SLACK_BOT_TOKEN")
    slack_channel_id = app.config.get("SLACK_CHANNEL_ID")

    slack_adapter = None
    if not slack_token:
        logging.warning(
            "SLACK_BOT_TOKEN not configured. Slack notifications will not be sent."
        )
    elif not slack_channel_id:
        logging.warning(
            "SLACK_CHANNEL_ID not configured. Slack notifications will not be sent."
        )
    else:
        try:
            slack_adapter = SlackNotificationAdapter(
                token=slack_token, channel_id=slack_channel_id
            )
        except ValueError as e:
            logging.error(f"Error initializing Slack adapter: {e}")
        except Exception as e:
            logging.error(
                f"Unexpected error initializing Slack adapter: {e}", exc_info=True
            )

    notification_channels = {
        "sales": slack_adapter,
        "pricing": email_adapter,
    }

    active_channels = {
        topic: adapter
        for topic, adapter in notification_channels.items()
        if adapter is not None
    }

    notification_channels = active_channels
    assistance_request_handler = HandleAssistanceRequest(active_channels)

    # Make the use case handler available
    # Routes can access this via current_app.assistance_request_handler
    app.assistance_request_handler = assistance_request_handler

    apifairy.init_app(app)
    ma.init_app(app)
    cache.init_app(app)

    # Import and Register Blueprints
    from .api import health_bp
    from .api import notify_bp

    app.register_blueprint(health_bp, url_prefix="/v1/health")
    app.register_blueprint(notify_bp, url_prefix="/v1/notify")

    return app
