from pydantic import BaseModel, Field


class ConversationRequest(BaseModel):
    message: str = Field(min_length=1)


class ProposedChange(BaseModel):
    field: str
    old_value: str | None = None
    new_value: str | None = None
    reason: str | None = None


class ConversationResponse(BaseModel):
    message: str
    changes: list[ProposedChange]
    requires_confirmation: bool = True