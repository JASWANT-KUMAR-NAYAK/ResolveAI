from typing import Optional

from pydantic import BaseModel


class DeviationData(BaseModel):
    site: Optional[str] = None
    date_of_occurrence: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    related_product: Optional[str] = None
    related_material: Optional[str] = None
    batch_number: Optional[str] = None
    process_parameter: Optional[str] = None


class ExtractRequest(BaseModel):
    text: str


class ExtractResponse(BaseModel):
    data: DeviationData

class AnalysisRequest(BaseModel):
    deviation: DeviationData


class ImpactAssessment(BaseModel):
    level: str
    reasoning: str


class SeverityAssessment(BaseModel):
    level: str
    reasoning: str


class AnalysisResponse(BaseModel):
    impact: ImpactAssessment
    severity: SeverityAssessment

class SaveDeviationData(BaseModel):
    site: str
    date_of_occurrence: str
    title: str
    description: str
    related_product: Optional[str] = None
    related_material: Optional[str] = None
    batch_number: Optional[str] = None
    process_parameter: Optional[str] = None


class SaveDeviationRequest(BaseModel):
    deviation: SaveDeviationData
    impact: Optional[ImpactAssessment] = None
    severity: Optional[SeverityAssessment] = None
    user_edits: Optional[dict] = None