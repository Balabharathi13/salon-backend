from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.analytics import AnalyticsModel
from app.utils.security import role_required

analytics_bp = Blueprint("analytics", __name__, url_prefix="/api/analytics")
analytics_model = AnalyticsModel()

# 📈 Shop Owner: View slot stats
@analytics_bp.route("/bookings", methods=["GET"])
@jwt_required()
@role_required("shop_owner")
def booking_stats():
    identity = get_jwt_identity()
    stats = analytics_model.get_booking_stats(identity["shop_id"])
    return jsonify(stats), 200

# 👷‍♀️ Worker performance
@analytics_bp.route("/workers", methods=["GET"])
@jwt_required()
@role_required("shop_owner")
def worker_stats():
    identity = get_jwt_identity()
    stats = analytics_model.get_worker_performance(identity["shop_id"])
    return jsonify(stats), 200

# 🧠 Admin-wide analytics (if needed)
@analytics_bp.route("/admin/bookings", methods=["GET"])
@jwt_required()
@role_required("admin")
def admin_booking_stats():
    pipeline = [
        {"$group": {
            "_id": "$shop_id",
            "total_bookings": {"$sum": 1}
        }}
    ]
    stats = list(analytics_model.bookings.aggregate(pipeline))
    return jsonify(stats), 200
