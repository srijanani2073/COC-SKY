from sqlalchemy import (
    Column, Integer, String, Boolean,
    DateTime, ForeignKey
)
from backend.db import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    full_name = Column(String)
    email = Column(String)
    password_hash = Column(String)
    role_id = Column(Integer, ForeignKey("roles.role_id"))
    is_active = Column(Boolean)
    created_at = Column(DateTime)
    last_login_at = Column(DateTime)