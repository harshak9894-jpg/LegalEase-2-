# LegalEase: AI-Powered Legal Document Generator

## Phase 2: Requirement Analysis

### 1. Introduction

LegalEase is an AI-powered legal document generation application designed to simplify the creation of structured legal-document drafts.

The system accepts user-provided information such as document type, parties involved, terms and conditions, and effective date. The information is processed through the backend and sent to the Gemini AI model for document generation.

The generated document is displayed to the user for preview and editing and can be downloaded in TXT, DOCX, or PDF format.

---

## 2. Functional Requirements

### FR-01: Document Type Input

The system shall allow the user to specify the type of legal document to be generated.

Examples include:

- Agreement
- Contract
- Non-Disclosure Agreement (NDA)
- Lease Agreement
- Employment Offer Letter

### FR-02: Parties Input

The system shall allow the user to provide information about the parties involved in the legal document.

Example:

- Service Provider and Client
- Tenant and Landlord
- Employee and Employer

### FR-03: Terms and Conditions Input

The system shall allow the user to enter the terms and conditions applicable to the document.

Multiple terms may be provided and separated into individual points.

### FR-04: Effective Date Input

The system shall allow the user to specify the effective date of the document.

### FR-05: Document Generation

The system shall send the provided information to the AI document-generation component and generate structured legal-document content.

### FR-06: Backend API

The system shall provide a FastAPI backend with a document-generation endpoint.

The `/generate` endpoint shall receive:

- document_type
- parties
- terms
- dates

### FR-07: AI Integration

The backend shall communicate with the Google Gemini AI model to generate the requested legal-document content.

### FR-08: Document Preview

The frontend shall display the generated document in a readable preview format.

### FR-09: Document Editing

The system shall allow users to edit the generated document before downloading it.

### FR-10: TXT Export

The system shall allow users to download the generated document as a plain-text `.txt` file.

### FR-11: DOCX Export

The system shall allow users to download the generated document as a formatted `.docx` file.

### FR-12: PDF Export

The system shall allow users to download the generated document as a formatted `.pdf` file.

### FR-13: Document Formatting

The generated DOCX and PDF documents shall support structured formatting such as:

- Document title
- Headings
- Paragraphs
- Terms table or bullet points
- Logo/branding
- Footer

---

## 3. Non-Functional Requirements

### NFR-01: Usability

The application should provide a simple and user-friendly interface so that users without a legal background can provide the required information.

### NFR-02: Performance

The application should process user requests and display generated content without unnecessary delay, subject to the response time of the Gemini API.

### NFR-03: Reliability

The system should handle invalid or incomplete inputs appropriately and avoid crashing during normal usage.

### NFR-04: Maintainability

The application should separate the frontend, backend, AI integration, document formatting, and testing components.

### NFR-05: Security

Sensitive configuration information such as the Gemini API key shall be stored using environment variables rather than directly inside the source code.

### NFR-06: Scalability

The backend architecture should allow the application to be extended with additional document types and features in the future.

### NFR-07: Compatibility

The application should operate in a modern web browser through the Streamlit interface.

---

## 4. User Requirements

The user should be able to:

1. Open the LegalEase application.
2. Select or enter a document type.
3. Enter the parties involved.
4. Enter the required terms and conditions.
5. Enter the effective date.
6. Generate a legal-document draft.
7. Preview the generated content.
8. Edit the generated content.
9. Download the document as TXT.
10. Download the document as DOCX.
11. Download the document as PDF.

---

## 5. Software Requirements

### Operating System

- Windows / Linux / macOS

### Programming Language

- Python 3.10 or higher

### Frameworks and Libraries

- FastAPI
- Uvicorn
- Streamlit
- Google Generative AI SDK
- python-docx
- FPDF
- Pillow
- Requests
- python-dotenv

### Development Environment

- Visual Studio Code or another Python-compatible IDE
- Python virtual environment
- Internet connection for Gemini API communication

---

## 6. Hardware Requirements

The project does not require specialized hardware.

Minimum requirements:

- Computer or laptop
- Minimum 4 GB RAM
- Modern processor
- Sufficient storage for Python environment and project files
- Internet connection for AI API requests

---

## 7. Input Requirements

The LegalEase application requires the following primary inputs:

| Input | Description |
|---|---|
| Document Type | Type of legal document to generate |
| Parties | Individuals or organizations involved |
| Terms | Terms and conditions of the document |
| Effective Date | Date on which the document becomes effective |

---

## 8. Output Requirements

The system shall produce:

### Generated Legal Content

AI-generated structured legal-document text.

### Preview

A readable preview of the generated document.

### Editable Content

The user shall be able to modify the generated content.

### Downloadable Documents

The system shall provide:

- `.txt`
- `.docx`
- `.pdf`

---

## 9. Backend API Requirements

The FastAPI backend shall provide a document-generation API.

### Endpoint

```text
POST /generate