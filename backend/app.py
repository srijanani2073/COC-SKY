from flask import Flask
from backend.db import engine, Base

from backend.models.case import Case
from backend.models.evidence import Evidence
from backend.models.user import User
from backend.models.role import Role
from backend.models.coc_log import CoCLog

print("REGISTERED TABLES:", Base.metadata.tables.keys())

from backend.routes.auth import auth_bp
from backend.routes.evidence import evidence_bp
from backend.routes.cases import cases_bp
from backend.routes.case_timeline import timeline_bp
from backend.routes.custody import custody_bp

app = Flask(__name__)

app.register_blueprint(auth_bp)
app.register_blueprint(evidence_bp)
app.register_blueprint(cases_bp)
app.register_blueprint(timeline_bp)
app.register_blueprint(custody_bp)

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    app.run(debug=True)