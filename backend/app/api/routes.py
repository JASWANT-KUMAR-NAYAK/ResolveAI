from app.schemas.conversation import ConversationRequest, ConversationResponse
from app.services.conversation_service import ConversationService

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.ai.extraction_chain import extraction_graph
from app.ai.analysis_chain import analysis_graph
from app.services.pdf_parser import extract_text_from_pdf
from app.db.database import get_db

from app.models.deviation import Deviation
from app.models.audit_log import AuditLog
from app.models.issue import Issue
from app.models.file import File as FileModel
from app.models.processing_job import ProcessingJob
from app.models.activity import Activity

from app.models.investigation import Investigation

from app.schemas.investigation import (
    InvestigationCreate,
    InvestigationUpdate,
    InvestigationResponse,
)

from app.schemas.file import FileResponse
from app.schemas.issue import IssueCreate, IssueResponse, IssueUpdate
from app.services.storage import StorageService



from app.schemas.deviation import (
    ExtractRequest,
    ExtractResponse,
    AnalysisRequest,
    AnalysisResponse,
    SaveDeviationRequest,
)

from app.schemas.issue import IssueCreate, IssueResponse


router = APIRouter(
    prefix="/api",
    tags=["Deviation"],
)


# ============================================================
# V1 - DEVIATION ROUTES
# ============================================================

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if file.content_type not in {"application/pdf", "text/plain"}:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported.",
        )

    contents = await file.read()

    if file.content_type == "application/pdf":
        text = extract_text_from_pdf(contents)
    else:
        text = contents.decode("utf-8", errors="ignore")

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="No readable text was found in the document.",
        )

    return {
        "filename": file.filename,
        "text": text,
    }


@router.post("/extract", response_model=ExtractResponse)
def extract_deviation(request: ExtractRequest):
    result = extraction_graph.invoke(
        {
            "text": request.text,
            "result": None,
            "error": None,
        }
    )

    if result["error"]:
        raise ValueError(result["error"])

    return {
        "data": result["result"],
    }


@router.post("/analyze", response_model=AnalysisResponse)
def analyze_deviation(request: AnalysisRequest):
    result = analysis_graph.invoke(
        {
            "deviation": request.deviation.model_dump(),
            "result": None,
            "error": None,
        }
    )

    if result["error"]:
        raise ValueError(result["error"])

    return result["result"]


@router.post("/save")
def save_deviation(
    request: SaveDeviationRequest,
    db: Session = Depends(get_db),
):
    data = request.deviation

    ai_recommendations = {
        "impact": request.impact.model_dump() if request.impact else None,
        "severity": request.severity.model_dump() if request.severity else None,
    }

    deviation = Deviation(
        site=data.site,
        date_of_occurrence=data.date_of_occurrence,
        title=data.title,
        description=data.description,
        related_product=data.related_product,
        related_material=data.related_material,
        batch_number=data.batch_number,
        process_parameter=data.process_parameter,
        ai_recommendations=ai_recommendations,
        user_edits=request.user_edits,
        status="submitted",
    )

    db.add(deviation)
    db.flush()

    audit = AuditLog(
        deviation_id=deviation.id,
        action="created",
        details="Deviation saved after AI-assisted review",
        changes=request.user_edits,
    )

    db.add(audit)
    db.commit()
    db.refresh(deviation)

    return {
        "id": deviation.id,
        "status": deviation.status,
        "message": "Deviation saved successfully",
    }


@router.get("/deviation/{deviation_id}")
def get_deviation(
    deviation_id: int,
    db: Session = Depends(get_db),
):
    deviation = db.get(Deviation, deviation_id)

    if not deviation:
        raise HTTPException(
            status_code=404,
            detail="Deviation not found",
        )

    return {
        "id": deviation.id,
        "created_at": deviation.created_at,
        "updated_at": deviation.updated_at,
        "site": deviation.site,
        "date_of_occurrence": deviation.date_of_occurrence,
        "title": deviation.title,
        "description": deviation.description,
        "related_product": deviation.related_product,
        "related_material": deviation.related_material,
        "batch_number": deviation.batch_number,
        "process_parameter": deviation.process_parameter,
        "ai_recommendations": deviation.ai_recommendations,
        "user_edits": deviation.user_edits,
        "status": deviation.status,
    }

# ============================================================
# V2 - ISSUE ROUTES
# ============================================================

@router.post("/issues", response_model=IssueResponse)
def create_issue(
    request: IssueCreate,
    db: Session = Depends(get_db),
):
    issue = Issue(
        title=request.title,
        description=request.description,
        location=request.location,
        occurred_at=request.occurred_at,
        affected_product=request.affected_product,
        affected_material=request.affected_material,
        reference_id=request.reference_id,
        affected_area=request.affected_area,
        category=request.category,
        priority=request.priority,
        business_impact=request.business_impact,
        status="NEW",
    )

    db.add(issue)
    db.commit()
    db.refresh(issue)

    return issue


@router.get("/issues/{issue_id}", response_model=IssueResponse)
def get_issue(
    issue_id: int,
    db: Session = Depends(get_db),
):
    issue = db.get(Issue, issue_id)

    if not issue:
        raise HTTPException(
            status_code=404,
            detail="Issue not found",
        )

    return issue

@router.get("/issues/{issue_id}", response_model=IssueResponse)
def get_issue(
    issue_id: int,
    db: Session = Depends(get_db),
):
    issue = db.get(Issue, issue_id)

    if not issue:
        raise HTTPException(
            status_code=404,
            detail="Issue not found",
        )

    return issue

@router.patch("/issues/{issue_id}", response_model=IssueResponse)
def update_issue(
    issue_id: int,
    request: IssueUpdate,
    db: Session = Depends(get_db),
):
    issue = db.get(Issue, issue_id)

    if not issue:
        raise HTTPException(
            status_code=404,
            detail="Issue not found",
        )

    update_data = request.model_dump(exclude_unset=True)

    changes = {}

    for field, new_value in update_data.items():
        old_value = getattr(issue, field)

        if old_value != new_value:
            changes[field] = {
                "old": old_value,
                "new": new_value,
            }

        setattr(issue, field, new_value)

    if changes:
        activity = Activity(
            issue_id=issue.id,
            actor_type="USER",
            actor_name="Demo User",
            action="ISSUE_UPDATED",
            details="Issue fields updated.",
            changes=changes,
        )

        db.add(activity)

    db.commit()
    db.refresh(issue)

    return issue

@router.post(
    "/issues/{issue_id}/files",
    response_model=FileResponse,
)
async def upload_issue_file(
    issue_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    issue = db.get(Issue, issue_id)

    if not issue:
        raise HTTPException(
            status_code=404,
            detail="Issue not found",
        )

    allowed_types = {
        "application/pdf",
        "text/plain",
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported.",
        )

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    filename = file.filename or "uploaded_file"

    storage = StorageService()

    storage_key = storage.save_file(
        contents=contents,
        filename=filename,
        issue_id=issue_id,
    )

    stored_file = FileModel(
        issue_id=issue_id,
        filename=filename,
        mime_type=file.content_type,
        storage_key=storage_key,
        size_bytes=len(contents),
    )

    db.add(stored_file)
    db.flush()

    processing_job = ProcessingJob(
        issue_id=issue_id,
        job_type="DOCUMENT_PROCESSING",
        status="PENDING",
    )

    db.add(processing_job)

    db.commit()
    db.refresh(stored_file)

    return stored_file

@router.get("/issues/{issue_id}/activities")
def get_issue_activities(
    issue_id: int,
    db: Session = Depends(get_db),
):
    issue = db.get(Issue, issue_id)

    if not issue:
        raise HTTPException(
            status_code=404,
            detail="Issue not found",
        )

    activities = (
        db.query(Activity)
        .filter(Activity.issue_id == issue_id)
        .order_by(Activity.created_at.desc())
        .all()
    )

    return activities

@router.post(
    "/issues/{issue_id}/conversation",
    response_model=ConversationResponse,
)
def propose_issue_change(
    issue_id: int,
    request: ConversationRequest,
    db: Session = Depends(get_db),
) -> ConversationResponse:
    issue = db.get(Issue, issue_id)

    if not issue:
        raise HTTPException(
            status_code=404,
            detail="Issue not found",
        )

    return ConversationService(db).propose_change(
        issue=issue,
        message=request.message,
    )
@router.post(
    "/issues/{issue_id}/investigation",
    response_model=InvestigationResponse,
)
def create_investigation(
    issue_id: int,
    request: InvestigationCreate,
    db: Session = Depends(get_db),
) -> InvestigationResponse:
    issue = db.get(Issue, issue_id)

    if not issue:
        raise HTTPException(
            status_code=404,
            detail="Issue not found",
        )

    investigation = Investigation(
        issue_id=issue_id,
        status="OPEN",
        ai_questions=request.ai_questions,
        probable_causes=request.probable_causes,
        findings=request.findings,
        root_cause=request.root_cause,
    )

    db.add(investigation)
    db.commit()
    db.refresh(investigation)

    return investigation

@router.get(
    "/issues/{issue_id}/investigation",
    response_model=InvestigationResponse,
)
def get_investigation(
    issue_id: int,
    db: Session = Depends(get_db),
) -> InvestigationResponse:
    issue = db.get(Issue, issue_id)

    if not issue:
        raise HTTPException(
            status_code=404,
            detail="Issue not found",
        )

    investigation = (
        db.query(Investigation)
        .filter(Investigation.issue_id == issue_id)
        .order_by(Investigation.created_at.desc())
        .first()
    )

    if not investigation:
        raise HTTPException(
            status_code=404,
            detail="Investigation not found",
        )

    return investigation



@router.patch(
    "/issues/{issue_id}/investigation",
    response_model=InvestigationResponse,
)
def update_investigation(
    issue_id: int,
    request: InvestigationUpdate,
    db: Session = Depends(get_db),
) -> InvestigationResponse:
    issue = db.get(Issue, issue_id)

    if not issue:
        raise HTTPException(
            status_code=404,
            detail="Issue not found",
        )

    investigation = (
        db.query(Investigation)
        .filter(Investigation.issue_id == issue_id)
        .order_by(Investigation.created_at.desc())
        .first()
    )

    if not investigation:
        raise HTTPException(
            status_code=404,
            detail="Investigation not found",
        )

    update_data = request.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(investigation, field, value)

    db.commit()
    db.refresh(investigation)

    return investigation