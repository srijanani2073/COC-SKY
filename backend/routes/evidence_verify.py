from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from backend.db import SessionLocal
from backend.models.evidence import Evidence
from backend.utils.hash_utils import compute_sha256
from backend.db.mongo import case_logs
from datetime import datetime

verify_bp = Blueprint("verify", __name__, url_prefix="/evidence")

@verify_bp.route("/verify/<int:evidence_id>", methods=["POST"])
def verify_evidence(evidence_id):
    role = request.headers.get("X-Role")
    user_id = int(request.headers.get("X-User-Id"))

    db: Session = SessionLocal()
    evidence = db.query(Evidence).filter(Evidence.evidence_id == evidence_id).first()

    if not evidence:
        db.close()
        return jsonify({"msg": "Evidence not found"}), 404

    recalculated_hash = compute_sha256(evidence)
    status = "VALID" if recalculated_hash == evidence.file_hash_sha256 else "TAMPERED"

    case_logs.insert_one({
        "case_id": evidence.case_id,
        "event_type": "EVIDENCE_VERIFICATION",
        "entity_type": "EVIDENCE",
        "entity_id": evidence_id,
        "performed_by": user_id,
        "role": role,
        "timestamp": datetime.utcnow(),
        "metadata": {
            "expected_hash": evidence.file_hash_sha256,
            "actual_hash": recalculated_hash,
            "status": status
        }
    })

    db.close()
    return jsonify({
        "evidence_id": evidence_id,
        "status": status
    })