from flask import jsonify
from . import health_bp


@health_bp.route("", methods=["GET"], strict_slashes=False)
def health():
    return jsonify({"status": "ok"}), 200
