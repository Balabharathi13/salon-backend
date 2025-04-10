from flask import Blueprint, request, jsonify
from app.schemas.auth import RegisterSchema, LoginSchema
from app.models.user import UserModel
from app.utils.security import hash_password, check_password, create_tokens
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

auth_bp = Blueprint('auth', __name__, url_prefix="/api/auth")

register_schema = RegisterSchema()
login_schema = LoginSchema()

@auth_bp.route('/register', methods=["POST"])
def register():
    data = request.get_json()
    errors = register_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    user_model = UserModel()  # ✅ Move here
    if user_model.find_by_email(data["email"]):
        return jsonify({"error": "Email already exists"}), 400

    data["password"] = hash_password(data["password"])
    user = user_model.create_user(data)
    return jsonify({"message": "Registered successfully"}), 201

@auth_bp.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    errors = login_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    user_model = UserModel()  # ✅ Move here
    user = user_model.find_by_email(data["email"])
    if not user or not check_password(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token, refresh_token = create_tokens(user["_id"], user["role"])
    user_model.update_token(user["_id"], refresh_token)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    })

@auth_bp.route('/refresh', methods=["POST",'GET'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({"access_token": access_token})
