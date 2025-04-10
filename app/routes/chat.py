from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from app.models.chat import (
    send_message,
    get_conversation
)

bp = Blueprint("chat", __name__, url_prefix="/api/chat")

# 🔄 Get chat between two users (Customer & Shop Owner)
@bp.route("/<user_id>", methods=["GET"])
@jwt_required()
def get_chat(user_id):
    current_user = get_jwt_identity()
    messages = get_conversation(current_user, user_id)
    return jsonify(messages), 200

# 💬 Send a chat message
@bp.route("/", methods=["POST"])
@jwt_required()
def post_message():
    data = request.json
    required = ["receiver_id", "message"]
    if not all(key in data for key in required):
        return jsonify({"error": "Missing fields"}), 400

    sender_id = get_jwt_identity()
    message_doc = {
        "sender_id": sender_id,
        "receiver_id": data["receiver_id"],
        "message": data["message"]
    }

    result = send_message(message_doc)
    return jsonify({"message": "Message sent", "id": str(result.inserted_id)}), 201
