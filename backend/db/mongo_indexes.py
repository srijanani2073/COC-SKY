from backend.db.mongo import db

def create_indexes():
    db.case_activity_logs.create_index("case_id")
    db.case_activity_logs.create_index("timestamp")

    db.evidence_metadata.create_index("evidence_id", unique=True)
    db.evidence_metadata.create_index("case_id")

    db.upload_logs.create_index("uploader_id")
    db.upload_logs.create_index("timestamp")

    db.custody_activity_logs.create_index("evidence_id")
    db.custody_activity_logs.create_index("timestamp")
    print("MongoDB indexes created")
    
if __name__ == "__main__":
    create_indexes()