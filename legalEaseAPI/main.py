import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from legalEaseAPI.routes import router

load_dotenv()

app = FastAPI(title="LegalEase - AI Legal Document Generator")

# Allow CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

# Root endpoint (Activity 3.1)
@app.get("/")
def home():
    return {"message": "Welcome to LegalEase AI Legal Document Generator API"}

@app.get("/health")
def health():
    return {"status": "ok", "service": "LegalEase API"}


# Run FastAPI if executed directly
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("BACKEND_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
