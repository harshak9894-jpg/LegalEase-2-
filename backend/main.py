from fastapi import FastAPI
from backend.routes import router


app = FastAPI(
    title="LegalEase - AI Legal Document Generator",
    description="Backend API for generating AI-powered legal document drafts.",
    version="1.0.0"
)


app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Welcome to LegalEase AI Legal Document Generator API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }