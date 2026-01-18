from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, BigInteger, Text
from backend.db import Base

class Evidence(Base):
    __tablename__ = "evidence"

    evidence_id = Column(Integer, primary_key=True)
    case_id = Column(Integer, ForeignKey("cases.case_id"), nullable=False)

    evidence_type = Column(String, nullable=False)
    evidence_tag = Column(String, nullable=True)

    uploader_id = Column(Integer, nullable=False)
    upload_time = Column(DateTime, nullable=False)

    original_filename = Column(String, nullable=True)
    content_mime = Column(String, nullable=True)
    size_bytes = Column(BigInteger, nullable=True)

    file_hash_sha256 = Column(String, nullable=True)

    encrypted = Column(Boolean, nullable=True)
    encryption_algo = Column(String, nullable=True)

    mongo_file_id = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, nullable=False)
    last_verified_at = Column(DateTime, nullable=True)

    version = Column(Integer, nullable=False, default=1)
    meta = Column("metadata", Text)