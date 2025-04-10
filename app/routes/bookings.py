from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.booking import BookingModel
from app.schemas.booking import BookingSchema
from app.utils.security import role_required
from bson import ObjectId

booking_bp = Blueprint("booking", __name__, url_prefix="/api/bookings")

booking_model = BookingModel()
booking_schema = BookingSchema()

# 📅 Customer: Create booking
@booking_bp.route("/", methods=["POST"])
@jwt_required()
@role_required("customer")
def create_booking():
    data = request.get_json()
    errors = booking_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    identity = get_jwt_identity()

    # Check for slot conflicts
    conflict = booking_model.get_bookings_by_slot(data["shop_id"], data["date"], data["slot"])
    if conflict:
        return jsonify({"error": "Slot not available"}), 409

    data["customer_id"] = identity["id"]
    data["status"] = "Booked"
    data["worker_id"] = None

    res = booking_model.create_booking(data)
    return jsonify({"message": "Booking successful", "booking_id": str(res.inserted_id)}), 201

# 📜 Customer: View bookings
@booking_bp.route("/my", methods=["GET"])
@jwt_required()
@role_required("customer")
def my_bookings():
    identity = get_jwt_identity()
    bookings = booking_model.get_bookings_by_customer(identity["id"])
    for b in bookings:
        b["_id"] = str(b["_id"])
        b["shop_id"] = str(b["shop_id"])
        if b.get("worker_id"):
            b["worker_id"] = str(b["worker_id"])
    return jsonify(bookings), 200

# 📊 Shop Owner: View bookings
@booking_bp.route("/shop/<shop_id>", methods=["GET"])
@jwt_required()
@role_required("shop_owner")
def shop_bookings(shop_id):
    bookings = booking_model.get_bookings_by_shop(shop_id)
    for b in bookings:
        b["_id"] = str(b["_id"])
        b["customer_id"] = str(b["customer_id"])
    return jsonify(bookings), 200

# 🔁 Shop Owner: Assign to worker
@booking_bp.route("/assign", methods=["PUT"])
@jwt_required()
@role_required("shop_owner")
def assign_worker():
    data = request.get_json()
    booking_id = data.get("booking_id")
    worker_id = data.get("worker_id")

    if not booking_id or not worker_id:
        return jsonify({"error": "Booking ID and Worker ID required"}), 400

    res = booking_model.assign_worker(booking_id, worker_id)
    if res.modified_count == 0:
        return jsonify({"error": "Booking not found"}), 404

    return jsonify({"message": "Worker assigned"}), 200

# ⏳ Status Update: Start/Complete
@booking_bp.route("/status", methods=["PUT"])
@jwt_required()
@role_required("shop_owner")
def update_status():
    data = request.get_json()
    booking_id = data.get("booking_id")
    status = data.get("status")

    if not booking_id or not status:
        return jsonify({"error": "Booking ID and status required"}), 400

    if status not in ["Started", "Completed"]:
        return jsonify({"error": "Invalid status"}), 400

    res = booking_model.update_status(booking_id, status)
    if res.modified_count == 0:
        return jsonify({"error": "Booking not found"}), 404

    return jsonify({"message": f"Booking marked as {status}"}), 200
