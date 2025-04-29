import os
import tempfile
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_caching import Cache
from apifairy import APIFairy
import logging

apifairy = APIFairy()
ma = Marshmallow()
logger = Logger(LogLevel.INFO)
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

    apifairy.init_app(app)
    ma.init_app(app)
    cache.init_app(app)

    from .api import tasks_api

    app.register_blueprint(tasks_api, url_prefix="/v1/tasks")

    return app
