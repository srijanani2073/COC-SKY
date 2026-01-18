from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from backend.db import SessionLocal
from backend.models.case import Case
from datetime import datetime
from backend.db.mongo import case_logs

cases_bp = Blueprint("cases", __name__, url_prefix="/cases")

def can_view(role):
    return role in ["admin", "investigator", "custodian", "auditor"]
def can_create(role):
    return role in ["admin", "investigator"]

# GET ALL CASES
@cases_bp.route("", methods=["GET"])
def list_cases():
    role = request.headers.get("X-Role")

    if not can_view(role):
        return jsonify({"msg": "Access denied"}), 403
    db: Session = SessionLocal()
    cases = db.query(Case).all()
    response = [
        {
            "case_id": c.case_id,
            "case_number": c.case_number,
            "title": c.title,
            "description": c.description,
            "status": c.status,
            "case_category": c.case_category,
            "external_case_ref": c.external_case_ref,
            "created_by": c.created_by,
            "created_at": c.created_at.isoformat() if c.created_at else None,
            "updated_at": c.updated_at.isoformat() if c.updated_at else None
        }
        for c in cases
    ]
    db.close()
    return jsonify(response)

# CREATE CASE
@cases_bp.route("", methods=["POST"])
def create_case():
    role = request.headers.get("X-Role")
    user_id = int(request.headers.get("X-User-Id"))

    if not can_create(role):
        return jsonify({"msg": "Access denied"}), 403
    data = request.get_json()
    status = data["status"].lower()
    allowed_statuses = {"open", "closed", "archived"}

    if status not in allowed_statuses:
        return jsonify({
            "msg": "Invalid status",
            "allowed": list(allowed_statuses)
        }), 400

    case = Case(
        case_number=data["case_number"],
        title=data["title"],
        description=data.get("description"),
        status=status,
        case_category=data.get("case_category"),
        external_case_ref=data.get("external_case_ref"),
        created_by=user_id,
        created_at=datetime.utcnow()
    )
    db: Session = SessionLocal()
    try:
        db.add(case)
        db.commit()
        db.refresh(case)
        case_logs.insert_one({
            "case_id": case.case_id,
            "event_type": "CASE_CREATED",
            "entity_type": "CASE",
            "entity_id": case.case_id,
            "performed_by": user_id,
            "role": role,
            "description": f"Case {case.case_number} created",
            "timestamp": datetime.utcnow(),
            "ip_address": request.remote_addr,
            "metadata": {
                "case_number": case.case_number,
                "title": case.title
            }
        })

    except IntegrityError:
        db.rollback()
        return jsonify({
            "msg": "Case number already exists",
            "case_number": data["case_number"]
        }), 409
    finally:
        db.close()

    return jsonify({
        "msg": "Case created",
        "case_id": case.case_id
    }), 201

# GET CASE BY ID
@cases_bp.route("/<int:case_id>", methods=["GET"])
def get_case(case_id):
    role = request.headers.get("X-Role")

    if not can_view(role):
        return jsonify({"msg": "Access denied"}), 403
    db: Session = SessionLocal()
    case = db.query(Case).filter(Case.case_id == case_id).first()
    if not case:
        db.close()
        return jsonify({"msg": "Case not found"}), 404

    response = {
        "case_id": case.case_id,
        "case_number": case.case_number,
        "title": case.title,
        "description": case.description,
        "status": case.status,
        "case_category": case.case_category,
        "external_case_ref": case.external_case_ref,
        "created_by": case.created_by,
        "created_at": case.created_at.isoformat() if case.created_at else None,
        "updated_at": case.updated_at.isoformat() if case.updated_at else None
    }
    db.close()
    return jsonify(response)

# UPDATE CASE STATUS
@cases_bp.route("/<int:case_id>/status", methods=["PUT"])
def update_case_status(case_id):
    role = request.headers.get("X-Role")
    user_id = int(request.headers.get("X-User-Id"))

    if role not in ["admin", "investigator"]:
        return jsonify({"msg": "Access denied"}), 403

    data = request.get_json()
    new_status = data["status"].lower()
    db: Session = SessionLocal()
    case = db.query(Case).filter(Case.case_id == case_id).first()

    if not case:
        db.close()
        return jsonify({"msg": "Case not found"}), 404

    old_status = case.status
    case.status = new_status
    case.updated_at = datetime.utcnow()
    db.commit()
    db.close()

    case_logs.insert_one({
        "case_id": case_id,
        "event_type": "STATUS_CHANGED",
        "from": old_status,
        "to": new_status,
        "performed_by": user_id,
        "role": role,
        "timestamp": datetime.utcnow()
    })
    return jsonify({"msg": "Status updated"})

@cases_bp.route("/<int:case_id>/timeline", methods=["GET"])
def get_case_timeline(case_id):
    role = request.headers.get("X-Role")

    if role not in ["admin", "investigator", "analyst", "viewer", "custodian"]:
        return jsonify({"msg": "Access denied"}), 403

    events = list(
        case_logs.find(
            {"case_id": case_id},
            {"_id": 0}
        ).sort("timestamp", 1)
    )
    return jsonify(events), 200