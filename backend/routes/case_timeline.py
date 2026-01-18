from flask import Blueprint, request, jsonify
from backend.db.mongo import case_logs

timeline_bp = Blueprint("timeline", __name__, url_prefix="/timeline")

@timeline_bp.route("/case/<int:case_id>", methods=["GET"])
def case_timeline(case_id):
    role = request.headers.get("X-Role")
    if role not in ["admin", "investigator", "custodian", "auditor"]:
        return jsonify({"msg": "Access denied"}), 403

    logs = case_logs.find(
        {"case_id": case_id},
        {"_id": 0}
    ).sort("timestamp", 1)

    return jsonify(list(logs))