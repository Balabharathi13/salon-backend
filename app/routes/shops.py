from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.shop import ShopModel
from app.schemas.shop import ShopRegisterSchema
from app.utils.security import role_required
from bson import ObjectId

shop_bp = Blueprint('shop', __name__, url_prefix="/api/shops")

shop_model = ShopModel()
shop_schema = ShopRegisterSchema()

# 🚀 Register Shop (Shop Owner)
@shop_bp.route('/register', methods=["POST"])
@jwt_required()
@role_required("shop_owner")
def register_shop():
    data = request.get_json()
    errors = shop_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    identity = get_jwt_identity()
    existing = shop_model.get_shop_by_owner(identity["id"])
    if existing:
        return jsonify({"error": "Shop already registered"}), 400

    data["owner_id"] = identity["id"]
    data["approved"] = False
    result = shop_model.register_shop(data)
    return jsonify({"message": "Shop registered. Awaiting admin approval.", "shop_id": str(result.inserted_id)}), 201

# 🌍 Discover shops nearby (Customer)
@shop_bp.route('/discover', methods=["GET"])
@jwt_required()
@role_required("customer")
def discover_shops():
    location = request.args.get("location")
    if not location:
        return jsonify({"error": "Location required"}), 400

    shops = shop_model.find_by_location(location)
    for s in shops:
        s["_id"] = str(s["_id"])
        s["owner_id"] = str(s["owner_id"])
    return jsonify(shops), 200

# ✅ Admin: Approve shop
@shop_bp.route('/approve/<shop_id>', methods=["PUT"])
@jwt_required()
@role_required("admin")
def approve_shop(shop_id):
    result = shop_model.approve_shop(shop_id)
    if result.modified_count == 0:
        return jsonify({"error": "Shop not found or already approved"}), 404
    return jsonify({"message": "Shop approved"}), 200

# 🧾 Admin: View all shops
@shop_bp.route('/all', methods=["GET"])
@jwt_required()
@role_required("admin")
def all_shops():
    shops = shop_model.get_all_shops()
    for s in shops:
        s["_id"] = str(s["_id"])
        s["owner_id"] = str(s["owner_id"])
    return jsonify(shops), 200
