from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import UserModel
from app.schemas.user import UserUpdateSchema
from app.utils.security import role_required
from bson import ObjectId

user_bp = Blueprint("user", __name__, url_prefix="/api/users")

user_model = UserModel()
user_update_schema = UserUpdateSchema()

# 🔐 Get current user profile
@user_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    identity = get_jwt_identity()
    user = user_model.find_by_id(identity["id"])
    if not user:
        return jsonify({"error": "User not found"}), 404

    user["_id"] = str(user["_id"])
    user.pop("password", None)
    user.pop("refresh_token", None)
    return jsonify(user), 200

# 🔧 Update user details (self-update only)
@user_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_user():
    identity = get_jwt_identity()
    user = user_model.find_by_id(identity["id"])
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    errors = user_update_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    user_model.collection.update_one(
        {"_id": ObjectId(identity["id"])},
        {"$set": data}
    )
    return jsonify({"message": "Profile updated successfully"}), 200

# 🔍 Admin: View all users
@user_bp.route("/all", methods=["GET"])
@jwt_required()
@role_required("admin")
def get_all_users():
    users = user_model.get_all_users()
    for u in users:
        u["_id"] = str(u["_id"])
        u.pop("password", None)
        u.pop("refresh_token", None)
    return jsonify(users), 200
