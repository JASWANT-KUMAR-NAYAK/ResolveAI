from sqlalchemy.orm import Session

from app.ai.investigation_chain import investigation_graph
from app.models.investigation import Investigation


class InvestigationService:
    def __init__(self, db: Session):
        self.db = db

    def generate_questions(
        self,
        investigation: Investigation,
        issue_context: str,
    ) -> list[str]:
        result = investigation_graph.invoke(
            {
                "issue_context": issue_context,
                "questions": [],
                "error": None,
            }
        )

        if result["error"]:
            raise ValueError(result["error"])

        questions = result["questions"]

        investigation.ai_questions = questions

        self.db.commit()
        self.db.refresh(investigation)

        return questions