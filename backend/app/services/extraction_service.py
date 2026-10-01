from sqlalchemy.orm import Session

from app.models.issue_extraction import IssueExtraction


class ExtractionService:
    def __init__(self, db: Session):
        self.db = db

    def save_extraction(
        self,
        issue_id: int,
        result: dict,
    ) -> list[IssueExtraction]:
        fields = [
            "location",
            "occurred_at",
            "title",
            "description",
            "affected_product",
            "affected_material",
            "reference_id",
            "affected_area",
        ]

        records = []

        for field_name in fields:
            value = result.get(field_name)

            if value is None:
                continue

            record = IssueExtraction(
                issue_id=issue_id,
                field_name=field_name,
                extracted_value=str(value),
                confidence=None,
                source_evidence=None,
            )

            self.db.add(record)
            records.append(record)

        self.db.commit()

        for record in records:
            self.db.refresh(record)

        return records