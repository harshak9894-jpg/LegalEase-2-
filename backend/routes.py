from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()


class DocumentRequest(BaseModel):
    document_type: str
    parties: str
    terms: str
    dates: str


@router.post("/generate")
def generate_document(request: DocumentRequest):
    return {
        "message": "Document generation request received",
        "document_type": request.document_type,
        "parties": request.parties,
        "terms": request.terms,
        "dates": request.dates,
    }