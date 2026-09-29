# LegalEase

LegalEase is an AI-assisted legal document drafting application.

It uses:

- Streamlit for the frontend
- FastAPI for the backend
- Gemini for AI document generation
- python-docx for DOCX generation
- FPDF for PDF generation

## Features

- AI-assisted legal document generation
- Document type input
- Parties input
- Terms and conditions
- Effective date
- Multiple languages
- Editable document preview
- TXT export
- DOCX export
- PDF export
- Logo branding
- Document footer
- FastAPI Swagger documentation
- Demo mode without API key

---

# Project Structure

```text
LegalEase/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   │
│   ├── ai_core/
│   │   ├── __init__.py
│   │   └── gemini_generator.py
│   │
│   └── document_utils/
│       ├── __init__.py
│       └── formatters.py
│
├── frontend/
│   └── app.py
│
├── assets/
│   └── logo.png
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md