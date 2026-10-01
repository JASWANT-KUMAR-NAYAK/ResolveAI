# AIVOA — AI-Powered Deviation Intake

An AI-assisted deviation intake module for pharmaceutical manufacturing.

The system helps users capture deviation information from a document or text input, automatically extract structured deviation data, assess potential impact and severity, allow human review and editing, and persist the final deviation in PostgreSQL with an audit record.

---

## Project Overview

The AIVOA Deviation Intake module is designed to reduce manual effort during deviation reporting.

A user can upload a deviation document or describe a deviation through the AI Copilot. The system then:

1. Extracts structured deviation information.
2. Populates the deviation intake form.
3. Assesses impact and severity using AI.
4. Allows the user to review and edit the extracted information.
5. Saves the reviewed deviation to PostgreSQL.
6. Creates an audit log entry for the saved deviation.

The workflow keeps a human reviewer in control of the final submitted information.

---

## Key Features

- AI-powered deviation information extraction
- PDF and TXT document upload
- Text-based deviation input
- Automatic form population
- Automatic deviation title generation
- AI impact assessment
- AI severity assessment
- Human review and editing
- PostgreSQL persistence
- Audit logging
- REST API using FastAPI
- LangGraph-based AI workflow
- Groq-powered LLM processing
- React + Redux frontend

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

## System Workflow

```text
Deviation PDF / TXT / User Text
              |
              v
       FastAPI Backend
              |
              v
      Document Text Extraction
              |
              v
       LangGraph Workflow
              |
              v
       Groq LLM Extraction
              |
              v
       Structured Deviation
              |
              v
        React + Redux Form
              |
              v
       Human Review / Edit
              |
              v
       AI Impact & Severity
              |
              v
        Save Deviation
              |
              v
         PostgreSQL
              |
              v
          Audit Log
```

---

## Deviation Fields

The system extracts and manages the following deviation fields:

| Field | Description |
|---|---|
| Site / Plant | Manufacturing site where the deviation occurred |
| Date of Occurrence | Date on which the deviation occurred |
| Title / Short Description | Concise description of the deviation |
| Detailed Description | Detailed description of the observed deviation |
| Related Product | Product affected by the deviation |
| Related Material | Material related to the deviation |
| Batch / Lot Number | Batch or lot associated with the deviation |
| Process Parameter Affected | Process parameter involved in the deviation |

These fields can be populated automatically by the AI and then reviewed or edited by the user.

---

## AI Extraction

The extraction workflow uses LangGraph to orchestrate the AI processing.

The extraction process:

1. Receives deviation text.
2. Sends the text to the Groq LLM.
3. Extracts structured deviation information.
4. Validates the returned information using Pydantic.
5. Returns the validated deviation data to the frontend.

The AI is instructed to:

- Extract only information explicitly present in the document.
- Avoid inventing missing information.
- Use `null` when information is unavailable.
- Preserve the meaning of the original text.
- Generate a concise title when an explicit title is not provided.
- Keep the batch number separate from the generated title.

---

## AI Assessment

After extraction, the deviation is analyzed for:

1. Impact
2. Severity

Both assessments use the following levels:

- Critical
- High
- Medium
- Low

### Impact

Impact represents the potential effect of the deviation on areas such as:

- Product quality
- Patient safety
- Regulatory compliance

The AI considers the available evidence and does not assume an impact that is not supported by the provided information.

### Severity

Severity represents the significance of the deviation itself.

The assessment considers information such as:

- Controlled process or parameter deviations
- Magnitude of the deviation
- Available consequences
- Mitigating information
- Whether the deviation was detected and corrected
- Whether product damage or adverse impact was reported

The AI is instructed not to assign a critical level without evidence supporting a critical event.

---

## Human-in-the-Loop

The system follows a human-in-the-loop workflow.

AI output is not treated as the final submission automatically.

The user can:

- Review extracted fields
- Edit extracted information
- Correct incorrect AI output
- Review impact assessment
- Review severity assessment
- Submit the final deviation

This allows the AI to assist the user while keeping the final decision and submitted information under human control.

---

## Frontend

The frontend is built using React and TypeScript.

Redux Toolkit manages the deviation intake state.

The application maintains state for:

### Document

- Uploaded file
- Extracted document text
- Upload status
- Document preview

### Extraction

- Extraction status
- Progress
- Extracted deviation data
- Confidence
- Errors

### Analysis

- Analysis status
- Impact level
- Impact reasoning
- Severity level
- Severity reasoning

### Form

- Current form values
- Dirty state
- User edits

---

## AI Copilot

The AI Copilot provides two ways to start a deviation intake:

### Text Input

The user can describe a deviation directly in the Copilot.

Example:

```text
A deviation occurred at Plant 1 involving a storage temperature
above the approved range for approximately 40 minutes.
```

The AI extracts the available structured information and populates the form.

### Document Upload

The user can upload:

- PDF
- TXT

The backend extracts readable text from the document before sending it to the AI extraction workflow.

---

## Backend

The backend is implemented using FastAPI.

The backend is responsible for:

- Receiving uploaded documents
- Extracting PDF text
- Processing deviation text
- Running LangGraph workflows
- Calling Groq
- Validating AI responses
- Performing impact and severity analysis
- Saving deviations
- Creating audit logs
- Retrieving saved deviations

---

## Database

The application uses PostgreSQL for persistence.

### `deviations`

The `deviations` table stores the final deviation information.

Important fields include:

- `id`
- `created_at`
- `updated_at`
- `site`
- `date_of_occurrence`
- `title`
- `description`
- `related_product`
- `related_material`
- `batch_number`
- `process_parameter`
- `extracted_fields`
- `ai_recommendations`
- `user_edits`
- `status`

### `audit_logs`

The `audit_logs` table stores audit information associated with deviation actions.

Important fields include:

- `id`
- `deviation_id`
- `action`
- `details`
- `changes`
- `created_at`

When a deviation is saved, the system creates an audit entry describing the action.

---

## API Endpoints

### Health Check

```http
GET /health
```

Used to verify that the backend is running.

### Upload Document

```http
POST /api/upload
```

Accepts PDF or TXT documents and extracts readable text.

### Extract Deviation

```http
POST /api/extract
```

Accepts deviation text and returns structured deviation information.

### Analyze Deviation

```http
POST /api/analyze
```

Analyzes a deviation and returns impact and severity assessments.

### Save Deviation

```http
POST /api/save
```

Saves the reviewed deviation to PostgreSQL and creates an audit log.

### Get Deviation

```http
GET /api/deviation/{deviation_id}
```

Retrieves a saved deviation by its database ID.

---

## Project Structure

```text
AIVOA/
│
├── backend/
│   │
│   ├── app/
│   │   ├── ai/
│   │   │   ├── analysis_chain.py
│   │   │   ├── analysis_prompt.py
│   │   │   ├── extraction_chain.py
│   │   │   ├── extraction_prompt.py
│   │   │   └── groq_client.py
│   │   │
│   │   ├── api/
│   │   │   └── routes.py
│   │   │
│   │   ├── db/
│   │   │   └── database.py
│   │   │
│   │   ├── models/
│   │   │   ├── deviation.py
│   │   │   └── audit_log.py
│   │   │
│   │   ├── schemas/
│   │   │   └── deviation.py
│   │   │
│   │   ├── services/
│   │   │   └── pdf_parser.py
│   │   │
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   │
│   ├── src/
│   │   ├── components/
│   │   │   ├── copilot/
│   │   │   │   └── AICopilot.tsx
│   │   │   │
│   │   │   └── deviation/
│   │   │       └── DeviationForm.tsx
│   │   │
│   │   ├── services/
│   │   │   └── api.ts
│   │   │
│   │   ├── store/
│   │   │   ├── deviationSlice.ts
│   │   │   └── store.ts
│   │   │
│   │   ├── types/
│   │   │   └── deviation.ts
│   │   │
│   │   ├── App.tsx
│   │   └── index.css
│   │
│   └── package.json
│
└── README.md
```

---

## Running the Application

### 1. Start PostgreSQL

Make sure the PostgreSQL server is running and the `aivioa_db` database exists.

### 2. Start the Backend

Open PowerShell:

```powershell
cd E:\AIVOA\backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

### 3. Start the Frontend

Open another PowerShell window:

```powershell
cd E:\AIVOA\frontend
npm run dev
```

The frontend will be available at:

```text
http://localhost:5173
```

---

## Example Deviation

Example input used during testing:

```text
Deviation Report

Site: Plant 1
Date of Occurrence: 27 September 2026

During routine monitoring at Plant 1, the storage temperature for Product A,
Batch B2409-15, increased above the approved range for approximately 40 minutes.

The excursion was detected by the monitoring system and the temperature was
restored to the approved range.

No visible product damage was observed.

Affected Process Parameter: Storage Temperature
Related Product: Product A
Batch Number: B2409-15
```

Expected extracted information includes:

| Field | Extracted Value |
|---|---|
| Site | Plant 1 |
| Date | 2026-09-27 |
| Title | Storage Temperature Excursion for Product A |
| Product | Product A |
| Batch | B2409-15 |
| Process Parameter | Storage Temperature |

The AI assessment can then provide impact and severity levels based only on the information available in the deviation.

---

## End-to-End Demo

The recommended demonstration flow is:

### Step 1 — Open the Application

Open:

```text
http://localhost:5173
```

### Step 2 — Upload the Deviation

Use the AI Copilot to upload the sample deviation PDF.

### Step 3 — Document Processing

The backend:

1. Receives the document.
2. Extracts its text.
3. Sends the text to the extraction workflow.
4. Uses Groq to generate structured information.
5. Validates the response.

### Step 4 — Form Population

The extracted information automatically appears in the deviation form.

### Step 5 — AI Assessment

The AI Copilot displays:

- Impact
- Severity
- Reasoning for both assessments

### Step 6 — Human Review

Edit a field if required.

For example, the user can modify the title or description before submission.

### Step 7 — Save

Click:

```text
Save Deviation
```

The backend stores the final information in PostgreSQL.

### Step 8 — Audit

The backend creates an audit log entry for the saved deviation.

---

## Testing and Verification

The following workflow has been tested:

- Backend health endpoint
- FastAPI Swagger interface
- TXT document upload
- PDF document upload
- PDF text extraction
- AI structured extraction
- Date normalization
- AI impact assessment
- AI severity assessment
- Redux form population
- Manual form editing
- Database persistence
- Audit log creation
- End-to-end save workflow

The application has successfully persisted test deviations in PostgreSQL and generated corresponding audit records.

---

## Current Status

The core AIVOA Deviation Intake workflow is implemented.

- [x] Project setup
- [x] React frontend
- [x] TypeScript
- [x] Redux Toolkit
- [x] FastAPI backend
- [x] PostgreSQL database
- [x] SQLAlchemy models
- [x] Groq integration
- [x] LangGraph extraction workflow
- [x] LangGraph analysis workflow
- [x] PDF parsing
- [x] TXT processing
- [x] Structured deviation extraction
- [x] Automatic form population
- [x] AI impact assessment
- [x] AI severity assessment
- [x] Human review and editing
- [x] Save workflow
- [x] PostgreSQL persistence
- [x] Audit logging
- [x] End-to-end testing
- [x] UI refinement
- [x] Demo workflow

---

## Limitations

The current implementation is an MVP focused on the deviation intake workflow.

### PDF Processing

Only machine-readable PDFs are currently supported.

Scanned or image-only PDFs require OCR, which is not currently implemented.

### Authentication

Authentication and role-based access control are not currently implemented.

### AI

AI-generated extraction and assessments should be reviewed by a human before submission.

### Production Deployment

The current application is designed as a local development and demonstration system and has not been production deployed.

### Automated Testing

The core workflow has been manually verified, but a comprehensive automated test suite has not yet been implemented.

---

## Future Improvements

Potential improvements include:

- OCR support for scanned PDFs
- Authentication
- Role-based access control
- Deviation listing and search
- Deviation history
- More detailed audit trails
- Advanced quality risk assessment
- Additional document formats
- Automated test coverage
- Production deployment
- Improved error handling
- Performance optimization
- More comprehensive validation

---

## Conclusion

AIVOA demonstrates an AI-assisted deviation intake workflow for pharmaceutical manufacturing.

The system combines:

- React
- Redux
- FastAPI
- PostgreSQL
- SQLAlchemy
- LangGraph
- Groq
- PDF text extraction

to create a workflow where unstructured deviation information can be converted into structured data, assessed by AI, reviewed by a human, and persisted with an audit record.

The primary design principle is:

**AI assists the deviation intake process, while the human remains in control of the final submitted information.**