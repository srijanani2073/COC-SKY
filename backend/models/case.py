from sqlalchemy import Column, Integer, String, Text, DateTime
from backend.db import Base
from datetime import datetime

class Case(Base):
    __tablename__ = "cases"

    case_id = Column(Integer, primary_key=True)
    case_number = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, nullable=False)

    case_category = Column(String)
    external_case_ref = Column(String)

    created_by = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime)

    meta = Column("metadata",Text)