from flask import jsonify
from . import health_bp


@health_bp.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200
