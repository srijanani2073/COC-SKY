from pymongo import MongoClient
from pymongo.server_api import ServerApi
from backend.config import MONGO_URI

client = MongoClient(
    MONGO_URI,
    server_api=ServerApi("1"),
    tls=True,
    tlsAllowInvalidCertificates=True,
    retryWrites=True
)

mongo_db = client["chainsky_meta"]

case_logs = mongo_db["case_activity_logs"]
evidence_logs = mongo_db["evidence_metadata"]
upload_logs = mongo_db["upload_logs"]
custody_logs = mongo_db["custody_activity_logs"]

def ping_mongo():
    client.admin.command("ping")
    print("MongoDB connected successfully")