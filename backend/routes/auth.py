from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from backend.db import SessionLocal
from backend.models.user import User
from backend.models.role import Role

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    db: Session = SessionLocal()
    result = (
        db.query(User, Role)
        .join(Role, User.role_id == Role.role_id)
        .filter(User.username == data["username"])
        .first()
    )
    if not result:
        return jsonify({"msg": "Invalid credentials"}), 401
    user, role = result
    if not user.is_active:
        return jsonify({"msg": "Account disabled"}), 403

    # TEMP – hashing added later
    if data["password"] != user.password_hash:
        return jsonify({"msg": "Invalid credentials"}), 401

    return jsonify({
        "user_id": user.user_id,
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email,
        "role": role.role_name 
    })