from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FileResponse(BaseModel):
    id: int
    issue_id: int
    filename: str
    mime_type: str | None
    size_bytes: int | None
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)