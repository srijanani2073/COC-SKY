from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from backend.db import Base
from datetime import datetime

class CoCLog(Base):
    __tablename__ = "coc_logs"
    log_id = Column(Integer, primary_key=True, index=True)

    evidence_id = Column(Integer, ForeignKey("evidence.evidence_id"), nullable=False)
    from_user_id = Column(Integer, ForeignKey("users.user_id"))
    to_user_id = Column(Integer, ForeignKey("users.user_id"))

    action = Column(String(30), nullable=False)
    action_description = Column(Text)
    location = Column(String(150))

    timestamp = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    reference_external = Column(String(100))
    signature_hex = Column(Text)
    signature_algo = Column(String(50))
    signature_verified = Column(Boolean, default=False)