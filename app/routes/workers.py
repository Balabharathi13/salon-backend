from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.worker import WorkerModel
from app.schemas.worker import WorkerSchema
from app.utils.security import role_required
from bson import ObjectId

worker_bp = Blueprint("workers", __name__, url_prefix="/api/workers")

worker_model = WorkerModel()
worker_schema = WorkerSchema()

# 👷 Add new worker
@worker_bp.route("/", methods=["POST"])
@jwt_required()
@role_required("shop_owner")
def add_worker():
    data = request.get_json()
    errors = worker_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    identity = get_jwt_identity()
    data["shop_id"] = identity["shop_id"]
    result = worker_model.add_worker(data)
    return jsonify({"message": "Worker added", "id": str(result.inserted_id)}), 201

# 📄 List workers
@worker_bp.route("/", methods=["GET"])
@jwt_required()
@role_required("shop_owner")
def list_workers():
    identity = get_jwt_identity()
    workers = worker_model.get_workers_by_shop(identity["shop_id"])
    for w in workers:
        w["_id"] = str(w["_id"])
    return jsonify(workers), 200

# ✏️ Edit worker
@worker_bp.route("/<worker_id>", methods=["PUT"])
@jwt_required()
@role_required("shop_owner")
def update_worker(worker_id):
    data = request.get_json()
    result = worker_model.update_worker(worker_id, data)
    if result.matched_count == 0:
        return jsonify({"error": "Worker not found"}), 404
    return jsonify({"message": "Worker updated"}), 200

# ❌ Delete worker
@worker_bp.route("/<worker_id>", methods=["DELETE"])
@jwt_required()
@role_required("shop_owner")
def delete_worker(worker_id):
    result = worker_model.delete_worker(worker_id)
    if result.deleted_count == 0:
        return jsonify({"error": "Worker not found"}), 404
    return jsonify({"message": "Worker deleted"}), 200
