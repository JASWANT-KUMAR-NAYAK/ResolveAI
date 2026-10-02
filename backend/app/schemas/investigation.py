from datetime import datetime

from pydantic import BaseModel, ConfigDict


class InvestigationCreate(BaseModel):
    ai_questions: list[str] | None = None
    probable_causes: list[str] | None = None
    findings: str | None = None
    root_cause: str | None = None


class InvestigationUpdate(BaseModel):
    status: str | None = None
    ai_questions: list[str] | None = None
    probable_causes: list[str] | None = None
    findings: str | None = None
    root_cause: str | None = None


class InvestigationResponse(BaseModel):
    id: int
    issue_id: int
    status: str
    ai_questions: list[str] | None
    probable_causes: list[str] | None
    findings: str | None
    root_cause: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)