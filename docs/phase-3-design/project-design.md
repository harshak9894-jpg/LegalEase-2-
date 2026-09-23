# LegalEase: AI-Powered Legal Document Generator

## Phase 3: Project Design

---

## 1. Design Overview

LegalEase is designed as a modular AI-powered application that separates the user interface, backend API, AI document generation, and document formatting responsibilities.

The application consists of the following major components:

1. Streamlit Frontend
2. FastAPI Backend
3. Gemini AI Integration
4. Document Formatting and Export Modules

The overall system follows this architecture:

User
  ↓
Streamlit Frontend
  ↓
FastAPI Backend
  ↓
Gemini AI Document Generator
  ↓
Generated Legal Document
  ↓
Preview / Edit
  ↓
TXT / DOCX / PDF Export

---

## 2. System Architecture

### 2.1 Architecture Components

### Frontend — Streamlit

The Streamlit frontend provides the user interface.

Responsibilities:

- Display the LegalEase interface.
- Collect document information.
- Accept document type.
- Accept parties involved.
- Accept terms and conditions.
- Accept effective date.
- Send the information to the backend.
- Display generated content.
- Allow editing of generated content.
- Provide document download options.

### Backend — FastAPI

The FastAPI backend acts as the application API layer.

Responsibilities:

- Receive requests from the Streamlit frontend.
- Validate incoming data.
- Provide the `/generate` API endpoint.
- Pass validated information to the AI document generator.
- Return generated document content to the frontend.

### AI Core — Gemini

The AI core communicates with the Google Gemini model.

Responsibilities:

- Receive structured document information.
- Construct an appropriate generation prompt.
- Request document generation from Gemini.
- Return the generated legal-document content.

### Document Formatting Modules

The formatting modules convert generated text into downloadable formats.

The application supports:

- TXT
- DOCX
- PDF

The DOCX and PDF outputs can include structured formatting, branding, headings, terms, and footer elements.

---

## 3. System Workflow

The complete workflow is:

### Step 1 — User Input

The user enters:

- Document type
- Parties involved
- Terms and conditions
- Effective date

### Step 2 — Streamlit Processing

The Streamlit frontend collects the user inputs and sends them to the FastAPI backend.

### Step 3 — API Request

The frontend sends a POST request to:

```text
/generate