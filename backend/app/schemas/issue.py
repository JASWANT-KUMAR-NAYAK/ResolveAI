from datetime import datetime

from pydantic import BaseModel, ConfigDict


class IssueCreate(BaseModel):
    title: str
    description: str
    location: str | None = None
    occurred_at: datetime | None = None
    affected_product: str | None = None
    affected_material: str | None = None
    reference_id: str | None = None
    affected_area: str | None = None
    category: str | None = None
    priority: str | None = None
    business_impact: str | None = None


class IssueUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    location: str | None = None
    occurred_at: datetime | None = None
    affected_product: str | None = None
    affected_material: str | None = None
    reference_id: str | None = None
    affected_area: str | None = None
    category: str | None = None
    priority: str | None = None
    business_impact: str | None = None


class IssueResponse(IssueCreate):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)