from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()
gemini_generator = GeminiDocumentGenerator()


class DocumentRequest(BaseModel):
    document_type: str
    parties: str
    terms: str
    dates: str
    language: Optional[str] = "English"
    api_key: Optional[str] = None
    model: Optional[str] = None


@router.post("/generate")
def generate_legal_document(request: DocumentRequest):
    try:
        response = gemini_generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates,
            language=request.language or "English",
            api_key=request.api_key,
            model=request.model,
        )
        return {"document": response}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
