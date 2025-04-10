from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.security import role_required
from app.models.notifications import (
    add_notification,
    get_user_notifications
)

bp = Blueprint("notifications", __name__, url_prefix="/api/notifications")

# ✅ Get all notifications for a user
@bp.route("/", methods=["GET"])
@jwt_required()
def get_notifications():
    user_id = get_jwt_identity()
    notifications = get_user_notifications(user_id)
    return jsonify(notifications), 200

# 🔧 Send a notification to a user (Admin or Shop Owner)
@bp.route("/", methods=["POST"])
@jwt_required()
@role_required(["admin", "shop_owner"])
def send_notification():
    data = request.json
    if not data.get("user_id") or not data.get("message"):
        return jsonify({"error": "user_id and message are required"}), 400

    sender_id = get_jwt_identity()
    notification_data = {
        "to_user_id": data["user_id"],
        "message": data["message"],
        "sender_id": sender_id
    }
    result = add_notification(notification_data)
    return jsonify({"message": "Notification sent", "id": str(result.inserted_id)}), 201
