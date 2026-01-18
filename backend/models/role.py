from sqlalchemy import Column, Integer, String, DateTime
from backend.db import Base

class Role(Base):
    __tablename__ = "roles"
    role_id = Column(Integer, primary_key=True)
    role_name = Column(String)
    description = Column(String)
    created_at = Column(DateTime)