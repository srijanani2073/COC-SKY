from backend.db.mongo import custody_logs

def get_next_custody_version(case_id, evidence_id):
    last = custody_logs.find_one(
        {
            "case_id": case_id,
            "evidence_id": evidence_id,
            "version": {"$exists": True}
        },
        sort=[("version", -1)]
    )

    return (last["version"] + 1) if last else 1