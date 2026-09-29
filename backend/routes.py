from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.ai_core.gemini_generator import GeminiDocumentGenerator


router = APIRouter()

generator = GeminiDocumentGenerator()


# ---------------------------------------------------------
# REQUEST MODEL
# ---------------------------------------------------------

class DocumentRequest(BaseModel):

    document_type: str = Field(
        ...,
        min_length=2,
        max_length=120,
        description="Type of legal document",
    )

    parties: str = Field(
        ...,
        min_length=2,
        max_length=5000,
        description="People or organizations involved",
    )

    terms: str = Field(
        ...,
        min_length=2,
        max_length=10000,
        description="Terms and conditions",
    )

    dates: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Effective date or relevant dates",
    )

    language: str = Field(
        default="English",
        min_length=2,
        max_length=50,
        description="Output language",
    )

    api_key: str | None = Field(
        default=None,
        description="Optional Gemini API key from frontend",
    )

    model: str | None = Field(
        default=None,
        description="Optional Gemini model override",
    )


# ---------------------------------------------------------
# RESPONSE MODEL
# ---------------------------------------------------------

class DocumentResponse(BaseModel):

    document: str

    model: str

    demo_mode: bool


# ---------------------------------------------------------
# GENERATE DOCUMENT
# ---------------------------------------------------------

@router.post(
    "/generate",
    response_model=DocumentResponse,
    tags=["Documents"],
)
def generate_legal_document(request: DocumentRequest):

    try:

        result = generator.generate_document(
            document_type=request.document_type.strip(),
            parties=request.parties.strip(),
            terms=request.terms.strip(),
            dates=request.dates.strip(),
            language=request.language.strip(),
            api_key=request.api_key.strip() if request.api_key else None,
            model=request.model.strip() if request.model else None,
        )

        return DocumentResponse(**result)

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Unexpected document-generation error: {exc}",
        ) from exc