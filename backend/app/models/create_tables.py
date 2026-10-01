from app.db.database import Base, engine
from app.models.deviation import Deviation
from app.models.audit_log import AuditLog

Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")