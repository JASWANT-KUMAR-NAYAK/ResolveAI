from pathlib import Path

from sqlalchemy.orm import Session

from app.models.file import File as FileModel
from app.models.processing_job import ProcessingJob


class DocumentProcessor:
    def __init__(self, db: Session):
        self.db = db

    def process_file(
        self,
        file_record: FileModel,
        job: ProcessingJob,
    ) -> str:
        job.status = "PROCESSING"
        job.attempts += 1

        self.db.commit()

        file_path = Path(file_record.storage_key)

        if not file_path.exists():
            job.status = "FAILED"
            job.last_error = "Stored file was not found."
            self.db.commit()

            raise FileNotFoundError(
                f"Stored file not found: {file_path}"
            )

        if file_record.mime_type == "application/pdf":
            from app.services.pdf_parser import extract_text_from_pdf

            contents = file_path.read_bytes()
            text = extract_text_from_pdf(contents)

        elif file_record.mime_type == "text/plain":
            text = file_path.read_text(
                encoding="utf-8",
                errors="ignore",
            )

        else:
            job.status = "FAILED" 
            job.last_error = "Unsupported file type."
            self.db.commit()

            raise ValueError("Unsupported file type.")

        if not text.strip():
            job.status = "FAILED"
            job.last_error = "No readable text was found."
            self.db.commit()

            raise ValueError(
                "No readable text was found in the document."
            )

        return text