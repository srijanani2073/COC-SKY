from backend.db.mongo import db

COLLECTIONS = [
    "case_activity_logs",
    "evidence_metadata",
    "upload_logs",
    "custody_activity_logs"
]

def setup_collections():
    existing = db.list_collection_names()
    for name in COLLECTIONS:
        if name not in existing:
            db.create_collection(name)
            print(f"Created collection: {name}")
        else:
            print(f"Collection already exists: {name}")

    db.command({
        "collMod": "case_activity_logs",
        "validator": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["case_id", "action", "performed_by", "timestamp"],
                "properties": {
                    "case_id": {
                        "bsonType": "int",
                        "description": "PostgreSQL case_id"
                    },
                    "action": {
                        "bsonType": "string",
                        "description": "Action performed on the case"
                    },
                    "performed_by": {
                        "bsonType": "int",
                        "description": "User ID"
                    },
                    "timestamp": {
                        "bsonType": "date"
                    },
                    "details": {
                        "bsonType": "string"
                    }
                }
            }
        },
        "validationLevel": "strict",
        "validationAction": "error"
    })
    print("✔ case_activity_logs validator applied")

    db.command({
    "collMod": "custody_activity_logs",
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["evidence_id", "from_role", "to_role", "timestamp"],
            "properties": {
                "evidence_id": {"bsonType": "int"},
                "from_role": {"bsonType": "string"},
                "to_role": {"bsonType": "string"},
                "timestamp": {"bsonType": "date"},
                "notes": {"bsonType": "string"}
            }
        }
    }
})
    print("✔ custody_activity_logs validator applied")

if __name__ == "__main__":
    setup_collections()