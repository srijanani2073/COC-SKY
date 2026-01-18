from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from backend.db import SessionLocal
from backend.models.evidence import Evidence
from backend.models.coc_log import CoCLog
from backend.utils.custody_utils import get_next_custody_version
from backend.db.mongo import custody_logs, case_logs
from datetime import datetime
from backend.utils.neo4j_utils import create_custody_event

custody_bp = Blueprint("custody", __name__, url_prefix="/custody")

def can_transfer(role):
    return role in ["admin", "investigator", "custodian"]

@custody_bp.route("/transfer", methods=["POST"])
def transfer_custody():
    role = request.headers.get("X-Role")
    user_id = int(request.headers.get("X-User-Id"))

    if not can_transfer(role):
        return jsonify({"msg": "Access denied"}), 403

    data = request.get_json()
    case_id = data["case_id"]
    evidence_id = data["evidence_id"]
    to_user = data["to_user"]
    location = data["location"]
    notes = data.get("notes")

    db: Session = SessionLocal()

    evidence = db.query(Evidence).filter(Evidence.evidence_id == evidence_id).first()
    if not evidence:
        db.close()
        return jsonify({"msg": "Invalid evidence"}), 404
    version = get_next_custody_version(case_id, evidence_id)

    #  POSTGRES — AUTHORITATIVE CHAIN OF CUSTODY
    coc = CoCLog(
        evidence_id=evidence_id,
        from_user_id=evidence.uploader_id,
        to_user_id=to_user,
        action="transfer",
        action_description=notes,
        location=location,
        timestamp=datetime.utcnow(),
        signature_verified=False
    )
    db.add(coc)
    db.commit()
    db.refresh(coc)

    # MONGODB — CUSTODY TIMELINE
    custody_logs.insert_one({
        "case_id": case_id,
        "evidence_id": evidence_id,
        "action": "TRANSFER",
        "from_user": evidence.uploader_id,
        "from_role": role,
        "to_user": to_user,
        "to_role": "custodian",
        "location": location,
        "notes": notes,
        "version": version,
        "timestamp": datetime.utcnow(),
        "ip_address": request.remote_addr
    })

    #  MONGODB — CASE TIMELINE
    case_logs.insert_one({
    "case_id": case_id,
    "action": "CUSTODY_TRANSFER",
    "entity_type": "EVIDENCE",
    "entity_id": evidence_id,
    "performed_by": user_id,
    "role": role,
    "timestamp": datetime.utcnow(),
    "metadata": {
        "to_user": to_user,
        "location": location,
        "version": version
    }})

    create_custody_event(
            case_id=case_id,
            evidence_id=evidence_id,
            custody_id=coc.log_id,  
            from_user=evidence.uploader_id,
            to_user=to_user,
            action="transfer",
            location=location,
            timestamp=datetime.utcnow()
        )
    db.close()

    return jsonify({
        "msg": "Custody transferred",
        "version": version,
        "coc_log_id": coc.log_id
    }), 201