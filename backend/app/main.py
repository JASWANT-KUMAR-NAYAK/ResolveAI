from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.deviation import DeviationData
from app.api.routes import router

app = FastAPI(
    title="ResolveAI",
    description="AI-powered Issue Intake, Triage and Resolution Platform",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "resolveai-backend",
    }

@app.post("/test/deviation")
def test_deviation(data: DeviationData):
    return {
        "message": "Deviation schema validated successfully",
        "data": data.model_dump(),
    }


app.include_router(router)