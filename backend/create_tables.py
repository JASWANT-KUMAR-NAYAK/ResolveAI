from app.db.database import Base, engine

from app.models.deviation import Deviation
from app.models.audit_log import AuditLog

from app.models.issue import Issue
from app.models.file import File
from app.models.processing_job import ProcessingJob
from app.models.issue_extraction import IssueExtraction
from app.models.ai_analysis import AIAnalysis
from app.models.investigation import Investigation
from app.models.action import Action
from app.models.activity import Activity
from app.models.similar_issue import SimilarIssue


Base.metadata.create_all(bind=engine)

print("All database tables created successfully.")