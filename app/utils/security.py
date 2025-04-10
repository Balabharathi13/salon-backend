from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, verify_jwt_in_request
from functools import wraps
from app.extensions import bcrypt
from flask import jsonify

def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(pw_hash, password):
    return bcrypt.check_password_hash(pw_hash, password)

def create_tokens(identity, role):
    access_token = create_access_token(identity={"id": str(identity), "role": role})
    refresh_token = create_refresh_token(identity={"id": str(identity), "role": role})
    return access_token, refresh_token

def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            identity = get_jwt_identity()
            if identity["role"] not in roles:
                return jsonify({"error": "Unauthorized"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
# from functools import wraps
# from flask import request, jsonify
# from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
# from werkzeug.security import generate_password_hash, check_password_hash
# from app.extensions import bcrypt
#
# # # 🔐 Password Hashing
# # def hash_password(password):
# #     return generate_password_hash(password)
#
# def verify_password(password, hashed):
#     return check_password_hash(hashed, password)
#
# def hash_password(password):
#     return bcrypt.generate_password_hash(password).decode('utf-8')
#
# def check_password(pw_hash, password):
#     return bcrypt.check_password_hash(pw_hash, password)
#
# # 🔑 JWT Token Generation
# def generate_tokens(user):
#     identity = {
#         "id": str(user["_id"]),
#         "role": user["role"],
#         "shop_id": str(user.get("shop_id", "")) if user["role"] == "shop_owner" else None
#     }
#     access = create_access_token(identity=identity)
#     refresh = create_refresh_token(identity=identity)
#     return {
#         "access_token": access,
#         "refresh_token": refresh,
#         "user": identity
#     }
#
# # 🛡️ Role-Based Access Decorator
# def role_required(*allowed_roles):
#     def decorator(f):
#         @wraps(f)
#         def wrapper(*args, **kwargs):
#             identity = get_jwt_identity()
#             if identity["role"] not in allowed_roles:
#                 return jsonify({"msg": "Access Denied: Insufficient permissions"}), 403
#             return f(*args, **kwargs)
#         return wrapper
#     return decorator
#
# # 🧹 Input Validation Placeholder (for future use)
# def sanitize_input(data):
#     if isinstance(data, dict):
#         return {k: str(v).strip() if isinstance(v, str) else v for k, v in data.items()}
#     return data
