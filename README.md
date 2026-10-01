# ResolveAI

AI-Powered Issue Intake, Triage & Resolution Platform.

ResolveAI is a portfolio-focused evolution of an earlier AI-assisted deviation intake prototype into a broader issue lifecycle management system.

The platform is designed to help users capture operational issues from text or documents, extract structured information with AI, review and edit the results, track processing, maintain activity history, and progressively support investigation, actions, and resolution.

---

## Project Status

ResolveAI V2 is currently under active development.

### Implemented

- [x] V2 project structure
- [x] FastAPI backend
- [x] React + TypeScript frontend
- [x] PostgreSQL database
- [x] SQLAlchemy models
- [x] Issue CRUD API
- [x] PDF/TXT file upload
- [x] Local file storage abstraction
- [x] Processing job records
- [x] Document text extraction
- [x] LangGraph issue extraction workflow
- [x] Groq LLM integration
- [x] Pydantic validation
- [x] Extraction persistence
- [x] Activity History
- [x] Conversational change proposals
- [x] Human confirmation boundary for proposed AI changes

### In Development / Planned

- [ ] Conversational change confirmation and mutation
- [ ] Backend-enforced issue status transitions
- [ ] Issue triage workflow
- [ ] Investigation workflow
- [ ] Root-cause analysis
- [ ] Corrective and preventive actions
- [ ] Similar issue search
- [ ] Dashboard and analytics
- [ ] Frontend V2 workflow
- [ ] Pagination and performance improvements
- [ ] Automated test coverage
- [ ] Docker/deployment setup
- [ ] Embedding-based semantic similarity
- [ ] Object-storage integration

---

## Product Vision

The target ResolveAI lifecycle is:

```text
Input
  ↓
File / Text Intake
  ↓
Storage
  ↓
Processing Job
  ↓
Document Processing
  ↓
AI Issue Extraction
  ↓
Validation
  ↓
Evidence / Confidence
  ↓
Triage
  ↓
Human Review
  ↓
Conversational Editing
  ↓
Investigation
  ↓
Root Cause
  ↓
Actions
  ↓
Resolution
  ↓
Activity History
  ↓
Analytics
```

The goal is to move from a simple AI extraction workflow toward a complete issue lifecycle platform while keeping humans in control of important decisions and changes.

---

## Core Concepts

### Issue

An Issue represents an operational incident, deviation, problem, or other event that requires review or resolution.

Current issue fields include:

- Title
- Description
- Location
- Occurred At
- Affected Product
- Affected Material
- Reference ID
- Affected Area
- Category
- Priority
- Business Impact
- Status

Current status values begin with:

```text
NEW
TRIAGED
INVESTIGATING
ACTION_REQUIRED
RESOLVED
CLOSED
```

Status transition enforcement is part of the V2 roadmap.

---

## AI-Assisted Document Processing

ResolveAI can accept supported documents and process them through the backend.

Current supported formats:

- PDF
- TXT

The processing pipeline is:

```text
Uploaded File
     ↓
StorageService
     ↓
ProcessingJob
     ↓
DocumentProcessor
     ↓
Text Extraction
     ↓
LangGraph
     ↓
Groq LLM
     ↓
Pydantic Validation
     ↓
Issue Extraction Records
```

The current extraction workflow identifies:

- Location
- Occurrence date
- Title
- Description
- Affected product
- Affected material
- Reference ID
- Affected area

The AI is instructed to extract only information supported by the source document and avoid inventing missing information.

---

## Human-in-the-Loop

AI output is not treated as an automatic final decision.

The intended workflow keeps a human reviewer between AI suggestions and important database mutations.

For example:

```text
User Request
     ↓
AI Interpretation
     ↓
Proposed Change
     ↓
Human Confirmation
     ↓
Controlled Mutation
     ↓
Activity History
```

The current conversational editing implementation already supports the proposal stage.

Example:

```text
User:
Change the priority to LOW

ResolveAI:
I prepared the requested change for review.

Priority:
HIGH → LOW

Confirmation required: true
```

The database is not modified during the proposal stage.

---

## Activity History

ResolveAI records issue changes through the `activities` table.

Activity records currently contain:

- Issue ID
- Actor type
- Actor name
- Action
- Details
- Changes
- Timestamp

Example change:

```json
{
  "priority": {
    "old": "LOW",
    "new": "HIGH"
  }
}
```

This provides a foundation for traceability and audit-oriented workflows.

---

## Database Architecture

ResolveAI uses PostgreSQL for structured application data.

Current V2 tables include:

```text
issues
files
processing_jobs
issue_extractions
ai_analyses
investigations
actions
activities
similar_issues
```

Legacy V1 tables remain in the development database while the V2 migration is being built:

```text
deviations
audit_logs
```

The V1 tables are retained temporarily to avoid disrupting the original implementation while V2 is developed.

---

## File Storage

Binary files are separated from structured database records.

The current architecture uses:

```text
StorageService
     ↓
Local Filesystem
```

The database stores file metadata such as:

- Filename
- MIME type
- Storage key
- File size
- Issue ID
- Upload timestamp

The storage layer is intentionally abstracted so that object storage can be introduced later without redesigning the Issue model.

---

## Backend Architecture

The backend follows a service-oriented FastAPI structure.

```text
backend/
│
├── app/
│   ├── ai/
│   │   ├── analysis_chain.py
│   │   ├── analysis_prompt.py
│   │   ├── extraction_chain.py
│   │   ├── extraction_prompt.py
│   │   ├── issue_extraction_chain.py
│   │   ├── issue_extraction_prompt.py
│   │   └── groq_client.py
│   │
│   ├── api/
│   │   └── routes.py
│   │
│   ├── db/
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── issue.py
│   │   ├── file.py
│   │   ├── processing_job.py
│   │   ├── issue_extraction.py
│   │   ├── ai_analysis.py
│   │   ├── investigation.py
│   │   ├── action.py
│   │   ├── activity.py
│   │   └── similar_issue.py
│   │
│   ├── schemas/
│   │   ├── issue.py
│   │   ├── file.py
│   │   ├── issue_extraction.py
│   │   └── conversation.py
│   │
│   ├── services/
│   │   ├── conversation_service.py
│   │   ├── document_processor.py
│   │   ├── extraction_service.py
│   │   ├── issue_processing_service.py
│   │   ├── pdf_parser.py
│   │   └── storage.py
│   │
│   └── main.py
│
├── create_tables.py
└── requirements.txt
```

---

## Frontend

The frontend is built with:

- React
- TypeScript
- Redux Toolkit
- React Redux
- Vite

The existing frontend currently contains the original V1 deviation-oriented components while the V2 backend architecture is being built.

The frontend will progressively migrate toward the ResolveAI Issue lifecycle workflow.

---

## API

### Health Check

```http
GET /health
```

Returns the backend service health status.

### Create Issue

```http
POST /api/issues
```

Creates a new Issue.

### Get Issue

```http
GET /api/issues/{issue_id}
```

Retrieves an Issue by ID.

### Update Issue

```http
PATCH /api/issues/{issue_id}
```

Updates Issue fields.

Changes are recorded in Activity History.

### Upload Issue File

```http
POST /api/issues/{issue_id}/files
```

Uploads a PDF or TXT document associated with an Issue.

The upload creates a processing job for document processing.

### Issue Activity History

```http
GET /api/issues/{issue_id}/activities
```

Retrieves the Issue's activity history.

### Conversational Editing

```http
POST /api/issues/{issue_id}/conversation
```

Accepts a natural-language change request and returns a proposed change.

Example:

```json
{
  "message": "Change the priority to LOW"
}
```

The response contains the proposed field change and whether confirmation is required.

---

## Technology Stack

### Frontend

- React
- TypeScript
- Redux Toolkit
- React Redux
- Vite

### Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL

### AI

- Groq
- `openai/gpt-oss-120b`
- LangGraph

### Document Processing

- pypdf

---

## Development Architecture

ResolveAI is intentionally being developed incrementally.

The current architectural priorities are:

1. Establish a reliable Issue data model.
2. Separate file storage from business data.
3. Represent asynchronous processing through ProcessingJob records.
4. Keep AI processing behind service boundaries.
5. Validate AI output with Pydantic.
6. Keep humans in control of AI-proposed changes.
7. Record important changes through Activity History.
8. Add advanced capabilities only after the core lifecycle is stable.

---

## Similar Issues

The planned similarity architecture starts with PostgreSQL full-text search.

Later iterations may introduce embeddings for semantic similarity.

Target workflow:

```text
Issue
  ↓
Search Existing Issues
  ↓
Candidate Similar Issues
  ↓
Similarity Score
  ↓
Human Review
```

Semantic embeddings are intentionally deferred until the basic search workflow is stable.

---

## Investigation

The planned investigation workflow will support:

- Investigation status
- AI-generated investigation questions
- Probable causes
- Findings
- Root cause

Target flow:

```text
Triaged Issue
     ↓
Investigation
     ↓
AI Questions
     ↓
Evidence / Findings
     ↓
Probable Causes
     ↓
Root Cause
```

---

## Actions

The planned Actions module will support:

- Corrective actions
- Preventive actions
- Action descriptions
- Owners
- Due dates
- Completion status
- Completion timestamps

Target flow:

```text
Root Cause
     ↓
Actions
     ↓
Owner
     ↓
Due Date
     ↓
Completion
```

---

## Testing

The project currently contains development-level tests and manual verification of the core backend workflows.

Verified areas include:

- Database connectivity
- FastAPI application startup
- Issue creation
- Issue retrieval
- Issue updates
- File upload
- File storage
- PDF extraction
- AI extraction
- Extraction persistence
- Processing jobs
- Activity History
- Conversational change proposals

A broader automated test suite will be added progressively as the architecture stabilizes.

---

## Local Development

### Backend

From the project root:

```powershell
cd E:\AIVOA-V2\backend
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Start FastAPI:

```powershell
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

### Frontend

Open another terminal:

```powershell
cd E:\AIVOA-V2\frontend
```

Install dependencies:

```powershell
npm install
```

Start the development server:

```powershell
npm run dev
```

The frontend normally runs at:

```text
http://localhost:5173
```

---

## Environment Variables

Secrets are kept outside the repository.

Example:

```env
GROQ_API_KEY=your_key_here
```

Do not commit `.env` files or API keys.

---

## Project Structure

```text
E:\AIVOA-V2
│
├── backend/
│   ├── app/
│   ├── create_tables.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── sample.pdf
├── sample_deviation.txt
├── README.md
└── .gitignore
```

---

## Development Roadmap

```text
V2 Foundation
      ↓
Issue CRUD
      ↓
File Storage
      ↓
Processing Jobs
      ↓
AI Extraction
      ↓
Activity History
      ↓
Conversational Editing
      ↓
Confirmation + Mutation
      ↓
Status Workflow
      ↓
Investigation
      ↓
Actions
      ↓
Similar Issues
      ↓
Dashboard
      ↓
Frontend V2
      ↓
Testing
      ↓
Deployment
```

---

## Current Milestone

ResolveAI V2 currently has a working backend foundation consisting of:

- Issue persistence
- File storage
- Processing jobs
- Document processing
- AI issue extraction
- Extraction persistence
- Activity History
- Conversational change proposals

The immediate next milestone is to implement the **confirmation and controlled mutation layer** for conversational editing.

---

## Design Principle

> AI assists the issue lifecycle; humans remain in control of important decisions and final changes.

ResolveAI is being developed as a portfolio project focused on practical AI engineering, backend architecture, human-in-the-loop workflows, traceability, and progressive system design.