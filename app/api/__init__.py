from flask import Blueprint
from flask_cors import CORS

health_bp = Blueprint("Health", __name__)
CORS(health_bp)
notify_bp = Blueprint("Notify", __name__)
CORS(notify_bp)

from . import health
from . import notify
