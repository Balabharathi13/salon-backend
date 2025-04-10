from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.security import role_required
from app.models.review import ReviewModel
from app.schemas.review import ReviewSchema

review_bp = Blueprint("reviews", __name__, url_prefix="/api/reviews")

review_model = ReviewModel()
review_schema = ReviewSchema()

# ⭐ Submit a review (Customer only)
@review_bp.route("/", methods=["POST"])
@jwt_required()
@role_required(["customer"])
def submit_review():
    user_id = get_jwt_identity()
    data = request.get_json()

    errors = review_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    review_data = {
        "shop_id": data["shop_id"],
        "rating": data["rating"],
        "comment": data.get("comment", ""),
        "customer_id": user_id,
    }

    result = review_model.add_review(review_data)
    return jsonify({"message": "Review submitted", "review_id": str(result.inserted_id)}), 201

# 📖 Get all reviews for a specific shop (Public)
@review_bp.route("/shop/<shop_id>", methods=["GET"])
def get_reviews(shop_id):
    reviews = review_model.get_reviews_by_shop(shop_id)
    return jsonify(reviews), 200
