from sqlalchemy.orm import Session

from app.models.file import File as FileModel
from app.models.processing_job import ProcessingJob
from app.services.document_processor import DocumentProcessor
from app.services.extraction_service import ExtractionService
from app.ai.issue_extraction_chain import issue_extraction_graph


class IssueProcessingService:
    def __init__(self, db: Session):
        self.db = db

    def process_job(
        self,
        job: ProcessingJob,
        file_record: FileModel,
    ) -> None:
        try:
            job.status = "PROCESSING"
            job.attempts += 1
            job.last_error = None
            self.db.commit()

            text = DocumentProcessor(self.db).process_file(
                file_record,
                job,
            )

            result = issue_extraction_graph.invoke(
                {
                    "text": text,
                    "result": None,
                    "error": None,
                }
            )

            if result["error"]:
                raise ValueError(result["error"])

            if result["result"] is None:
                raise ValueError("AI extraction returned no result.")

            ExtractionService(self.db).save_extraction(
                issue_id=job.issue_id,
                result=result["result"],
            )

            job.status = "COMPLETED"
            job.completed_at = __import__("datetime").datetime.utcnow()
            self.db.commit()

        except Exception as exc:
            job.status = "FAILED"
            job.last_error = str(exc)
            self.db.commit()

            raise