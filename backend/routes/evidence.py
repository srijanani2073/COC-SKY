from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from backend.db import SessionLocal
from backend.models.evidence import Evidence
from backend.models.case import Case
from backend.utils.hash_utils import compute_sha256
from datetime import datetime
from backend.db.mongo import evidence_logs, upload_logs, case_logs
from backend.utils.neo4j_utils import get_custody_graph

evidence_bp = Blueprint("evidence", __name__, url_prefix="/evidence")

# RBAC HELPERS
def can_upload(role):
    return role in ["admin", "investigator"]
def can_view(role):
    return role in ["admin", "investigator", "custodian", "auditor"]

# VERSIONING HELPER
def get_next_version(db, case_id, original_filename):
    last = (
        db.query(Evidence)
        .filter(
            Evidence.case_id == case_id,
            Evidence.original_filename == original_filename
        )
        .order_by(Evidence.version.desc())
        .first()
    )
    return (last.version + 1) if last else 1

# UPLOAD EVIDENCE (VERSIONED)
@evidence_bp.route("/upload", methods=["POST"])
def upload_evidence():
    role = request.headers.get("X-Role")
    user_id = int(request.headers.get("X-User-Id"))
    user_id_raw = request.headers.get("X-User-Id")

    if not role or not user_id_raw:
        return jsonify({
            "msg": "Missing authentication headers",
            "required": ["X-Role", "X-User-Id"]
        }), 400

    try:
        user_id = int(user_id_raw)
    except ValueError:
        return jsonify({"msg": "Invalid X-User-Id"}), 400

    if not can_upload(role):
        return jsonify({"msg": "Access denied"}), 403
    db: Session = SessionLocal()

    try:
        case_id = int(request.form.get("case_id"))
        evidence_type = request.form.get("evidence_type").lower()
        file = request.files.get("file")

        if not file:
            return jsonify({"msg": "File required"}), 400

        case = db.query(Case).filter(Case.case_id == case_id).first()
        if not case:
            return jsonify({"msg": "Invalid case"}), 404

        file_bytes = file.read()
        file_hash = compute_sha256(file_bytes)
        version = get_next_version(db, case_id, file.filename)

        evidence = Evidence(
            case_id=case_id,
            evidence_type=evidence_type,
            uploader_id=user_id,
            upload_time=datetime.utcnow(),
            original_filename=file.filename,
            content_mime=file.mimetype,
            size_bytes=len(file_bytes),
            file_hash_sha256=file_hash,
            encrypted=True,
            encryption_algo="AES-256",
            mongo_file_id="PENDING",
            is_active=True,
            created_at=datetime.utcnow(),
            last_verified_at=None,
            version=version,
            metadata="{}" 
        )

        db.add(evidence)
        db.commit()
        db.refresh(evidence)

        # MONGO LOGGING (BEST EFFORT)
        try:
            case_logs.insert_one({
                "case_id": case_id,
                "action": "EVIDENCE_UPLOADED",
                "performed_by": user_id,
                "timestamp": datetime.utcnow(),
                "details": f"Evidence uploaded (v{version}): {file.filename}"
            })

            evidence_logs.insert_one({
                "evidence_id": evidence.evidence_id,
                "case_id": case_id,
                "evidence_type": evidence_type,
                "file_hash_sha256": file_hash,
                "original_filename": file.filename,
                "content_mime": file.mimetype,
                "size_bytes": len(file_bytes),
                "uploaded_by": user_id,
                "uploaded_at": datetime.utcnow(),
                "version": version,
                "is_active": True
            })

            upload_logs.insert_one({
                "case_id": case_id,
                "evidence_id": evidence.evidence_id,
                "action": "UPLOAD",
                "performed_by": user_id,
                "role": role,
                "timestamp": datetime.utcnow(),
                "ip_address": request.remote_addr
            })

        except Exception as mongo_err:
            print("[WARN] Mongo logging failed:", mongo_err)

        return jsonify({
            "msg": "Evidence uploaded",
            "evidence_id": evidence.evidence_id,
            "version": version,
            "hash": file_hash
        }), 201

    except IntegrityError:
        db.rollback()

        # DUPLICATE HASH — LOG SAFELY
        try:
            upload_logs.insert_one({
                "case_id": case_id,
                "action": "DUPLICATE_UPLOAD_BLOCKED",
                "performed_by": user_id,
                "role": role,
                "file_hash_sha256": file_hash,
                "timestamp": datetime.utcnow(),
                "ip_address": request.remote_addr
            })

            case_logs.insert_one({
                "case_id": case_id,
                "action": "DUPLICATE_EVIDENCE_ATTEMPT",
                "performed_by": user_id,
                "timestamp": datetime.utcnow(),
                "metadata": {
                    "file_hash_sha256": file_hash
                }
            })

        except Exception as mongo_err:
            print("[WARN] Mongo duplicate log failed:", mongo_err)

        return jsonify({
            "msg": "Duplicate evidence detected",
            "reason": "Same file hash already exists for this case"
        }), 409

    finally:
        db.close()


# LIST EVIDENCE FOR A CASE
@evidence_bp.route("/case/<int:case_id>", methods=["GET"])
def list_evidence(case_id):
    role = request.headers.get("X-Role")

    if not can_view(role):
        return jsonify({"msg": "Access denied"}), 403
    db: Session = SessionLocal()
    evidence_items = (
        db.query(Evidence)
        .filter(Evidence.case_id == case_id, Evidence.is_active == True)
        .order_by(Evidence.version.asc())
        .all()
    )
    response = [
        {
            "evidence_id": e.evidence_id,
            "filename": e.original_filename,
            "type": e.evidence_type,
            "hash": e.file_hash_sha256,
            "version": e.version,
            "uploaded_at": e.upload_time
        }
        for e in evidence_items
    ]

    db.close()
    return jsonify(response)

@evidence_bp.route("/case/<int:case_id>/list", methods=["GET"])
def list_case_evidence(case_id):
    role = request.headers.get("X-Role")

    if role not in ["admin", "investigator", "analyst", "viewer", "custodian"]:
        return jsonify({"msg": "Access denied"}), 403
    db = SessionLocal()

    items = (
        db.query(Evidence)
        .filter(Evidence.case_id == case_id, Evidence.is_active == True)
        .order_by(Evidence.upload_time.asc())
        .all()
    )
    result = [
        {
            "evidence_id": e.evidence_id,
            "filename": e.original_filename,
            "type": e.evidence_type,
            "version": e.version,
            "hash": e.file_hash_sha256,
            "uploaded_at": e.upload_time
        }
        for e in items
    ]
    db.close()
    return jsonify(result), 200

@evidence_bp.route("/<int:evidence_id>/custody-graph", methods=["GET"])
def view_custody_graph(evidence_id):
    role = request.headers.get("X-Role")

    if role not in ["admin", "investigator", "custodian", "auditor"]:
        return jsonify({"msg": "Access denied"}), 403

    graph = get_custody_graph(evidence_id)
    return jsonify(graph), 200