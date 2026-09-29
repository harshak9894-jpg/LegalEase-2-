from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import router


app = FastAPI(
    title="LegalEase - AI Legal Document Generator",
    description=(
        "AI-assisted legal document drafting API using Gemini, "
        "with TXT, DOCX and PDF export support."
    ),
    version="1.0.0",
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# API ROUTES
# ---------------------------------------------------------

app.include_router(router)


# ---------------------------------------------------------
# ROOT
# ---------------------------------------------------------

@app.get("/", tags=["System"])
def root():
    return {
        "message": "Welcome to LegalEase AI Legal Document Generator API",
        "status": "running",
        "docs": "/docs",
        "health": "/health",
    }


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get("/health", tags=["System"])
def health():
    return {
        "status": "ok",
        "service": "LegalEase API",
    }


# ---------------------------------------------------------
# RUN DIRECTLY
# ---------------------------------------------------------

if __name__ == "__main__":
    import os
    import uvicorn
    from dotenv import load_dotenv

    load_dotenv()
    port = int(os.getenv("BACKEND_PORT", 8001))

    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=port,
        reload=True,
    )