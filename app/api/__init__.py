from flask import Blueprint
from flask_cors import CORS

tasks_api = Blueprint("Tasks", __name__)
CORS(tasks_api)

from . import tasks
