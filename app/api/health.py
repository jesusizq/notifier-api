from flask import jsonify
from . import tasks_api as api


@api.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200
