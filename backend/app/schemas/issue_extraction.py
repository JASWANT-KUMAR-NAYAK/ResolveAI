from pydantic import BaseModel


class IssueExtractionResult(BaseModel):
    location: str | None = None
    occurred_at: str | None = None
    title: str | None = None
    description: str | None = None
    affected_product: str | None = None
    affected_material: str | None = None
    reference_id: str | None = None
    affected_area: str | None = None