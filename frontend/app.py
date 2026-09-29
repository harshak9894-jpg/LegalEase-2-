import os
import sys
from datetime import date
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv

# ---------------------------------------------------------
# PATH SETUP
# ---------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8001")
DEFAULT_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()

# ---------------------------------------------------------
# IMPORT FORMATTERS & BACKEND AI
# ---------------------------------------------------------
from backend.document_utils.formatters import (
    format_docx,
    format_html_preview,
    format_pdf,
    sanitize_text,
    text_bytes,
)
from ai_core.gemini_generator import GeminiDocumentGenerator

generator = GeminiDocumentGenerator()

# ---------------------------------------------------------
# STREAMLIT CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="LegalEase - AI-Powered Legal Document Generator",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# CUSTOM CSS MATCHING USER UI SCREENSHOT
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Container sizing */
    .main .block-container {
        max-width: 1280px;
        padding-top: 1rem;
        padding-bottom: 3rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* Top Navbar */
    .navbar-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.8rem 0;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid #E5E7EB;
    }
    .brand-group {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .brand-logo-icon {
        font-size: 2.2rem;
        line-height: 1;
        color: #1E3A8A;
    }
    .brand-name {
        font-size: 1.6rem;
        font-weight: 700;
        color: #111827;
        margin: 0;
        line-height: 1.2;
    }
    .brand-sub {
        font-size: 0.85rem;
        color: #6B7280;
        margin: 0;
    }
    .nav-links {
        display: flex;
        align-items: center;
        gap: 18px;
    }
    .nav-item {
        font-size: 0.92rem;
        font-weight: 500;
        color: #374151;
        text-decoration: none;
        padding: 6px 12px;
        border-radius: 6px;
        transition: all 0.2s;
        cursor: pointer;
    }
    .nav-item:hover {
        background: #F3F4F6;
        color: #1E40AF;
    }
    .demo-pill {
        background: #111827;
        color: #F9FAFB;
        font-size: 0.82rem;
        font-weight: 600;
        padding: 6px 14px;
        border-radius: 20px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .demo-dot {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        display: inline-block;
    }

    /* Form Card (Left Column) */
    .form-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .form-card-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 4px;
    }
    .form-card-subtitle {
        font-size: 0.88rem;
        color: #6B7280;
        margin-bottom: 20px;
    }
    .char-counter {
        font-size: 0.75rem;
        color: #9CA3AF;
        text-align: right;
        margin-top: -12px;
        margin-bottom: 8px;
    }

    /* Gradient Generate Button */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #4F46E5 0%, #7C3AED 100%) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.65rem 1.5rem !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(79, 70, 229, 0.4) !important;
    }

    /* Document Sheet (Right Column) */
    .success-alert {
        background-color: #ECFDF5;
        border: 1px solid #A7F3D0;
        color: #065F46;
        padding: 12px 16px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.92rem;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 16px;
    }
    .document-paper {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 36px 42px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        max-height: 600px;
        overflow-y: auto;
        color: #1F2937;
        line-height: 1.7;
        font-size: 0.95rem;
    }
    .document-paper h2 {
        text-align: center;
        font-size: 1.5rem;
        font-weight: 700;
        color: #111827;
        letter-spacing: 0.5px;
        margin-bottom: 24px;
        border-bottom: 2px solid #111827;
        padding-bottom: 8px;
    }
    .document-paper h3 {
        font-size: 1.1rem;
        font-weight: 700;
        color: #111827;
        margin-top: 18px;
        margin-bottom: 8px;
    }
    .document-paper p {
        margin-bottom: 12px;
    }
    .document-paper strong {
        color: #111827;
    }

    /* Action Buttons in Document Preview */
    .btn-action-row {
        display: flex;
        gap: 8px;
        margin-bottom: 16px;
    }

    /* Bottom Features Footer */
    .footer-features {
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 1px solid #E5E7EB;
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
    }
    .feature-card {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 12px;
        background: #F9FAFB;
        border: 1px solid #F3F4F6;
        border-radius: 8px;
    }
    .feature-icon {
        font-size: 1.6rem;
        color: #4F46E5;
    }
    .feature-title {
        font-size: 0.92rem;
        font-weight: 700;
        color: #111827;
        margin: 0;
    }
    .feature-desc {
        font-size: 0.78rem;
        color: #6B7280;
        margin: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# SESSION STATE INITIALIZATION
# ---------------------------------------------------------
if "generated_doc" not in st.session_state:
    st.session_state["generated_doc"] = None
if "edit_mode" not in st.session_state:
    st.session_state["edit_mode"] = False
if "demo_mode" not in st.session_state:
    st.session_state["demo_mode"] = False
if "doc_type" not in st.session_state:
    st.session_state["doc_type"] = "Freelance Work Contract"

# Pre-populate with faculty example on initial load
DEFAULT_PARTIES = "Jane Doe (Service Provider), TechNova Inc. (Client)"
DEFAULT_TERMS = (
    "•Payment within 30 days;\n"
    "•Confidentiality must be maintained;\n"
    "•The provider agrees to deliver the work by the agreed deadline;\n"
    "•Either party may terminate with 15 days notice."
)
DEFAULT_DATE = "September 29, 2026"

# ---------------------------------------------------------
# TOP NAVBAR
# ---------------------------------------------------------
mode_label = "🟢 Demo Mode" if st.session_state["demo_mode"] else "⚡ Live AI Mode"

st.markdown(
    f"""
    <div class="navbar-container">
        <div class="brand-group">
            <span class="brand-logo-icon">⚖️</span>
            <div>
                <h1 class="brand-name">LegalEase</h1>
                <p class="brand-sub">AI-Powered Legal Document Generator</p>
            </div>
        </div>
        <div class="nav-links">
            <span class="nav-item">🏠 Home</span>
            <span class="nav-item">ℹ️ About</span>
            <span class="nav-item">Features</span>
            <span class="nav-item">❓ Help</span>
            <div class="demo-pill">
                <span class="demo-dot"></span>
                <span>{mode_label}</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# SIDEBAR (For Configuration & Faculty Details)
# ---------------------------------------------------------
with st.sidebar:
    st.header("⚙️ LegalEase Settings")
    st.markdown("Faculty Project Reference: **SmartBridge / SmartInternz**")
    
    st.divider()
    st.session_state["demo_mode"] = st.toggle("Enable Demo Mode (Offline)", value=st.session_state["demo_mode"])
    
    api_key_input = st.text_input(
        "Google Gemini API Key",
        value=DEFAULT_API_KEY,
        type="password",
        help="Google AI Studio Gemini API Key",
    )
    
    selected_model = st.selectbox(
        "AI Model",
        ["gemini-3.8-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
        index=0,
        help="gemini-3.8-flash works directly with current Google AI Studio keys; gemini-1.5-pro as in faculty PDF.",
    )

    st.divider()
    st.markdown("### 📚 Reference Resources")
    st.markdown("- [FastAPI Backend](http://127.0.0.1:8000/docs)")
    st.markdown("- [YouTube Faculty Demo](https://youtu.be/cDqpyNz3GpI)")

# ---------------------------------------------------------
# MAIN TWO-COLUMN LAYOUT
# ---------------------------------------------------------
col_left, col_right = st.columns([1, 1.25], gap="large")

with col_left:
    st.markdown('<div class="form-card-title">Create Your Legal Document</div>', unsafe_allow_html=True)
    st.markdown('<div class="form-card-subtitle">Fill in the details below to generate your document.</div>', unsafe_allow_html=True)

    # Document Type Dropdown
    doc_types = [
        "Freelance Work Contract",
        "Non-Disclosure Agreement (NDA)",
        "Residential Lease Agreement",
        "Employment Contract",
        "Partnership Agreement",
        "Custom Legal Agreement",
    ]
    doc_type_val = st.selectbox("Document Type *", doc_types, index=0)

    # Auto-fill defaults if preset matches
    current_parties = DEFAULT_PARTIES
    current_terms = DEFAULT_TERMS
    if doc_type_val == "Non-Disclosure Agreement (NDA)":
        current_parties = "Alpha Corp (Disclosing Party), Beta Solutions Ltd (Receiving Party)"
        current_terms = (
            "•Confidential Information includes trade secrets, source code, and business plans;\n"
            "•Receiving Party shall hold information in strict confidence for 3 years;\n"
            "•No disclosure to third parties without prior written consent;\n"
            "•Immediate return of all materials upon request."
        )
    elif doc_type_val == "Residential Lease Agreement":
        current_parties = "Alice Smith (Tenant), XYZ Realty Management (Landlord)"
        current_terms = (
            "•Lease term of 12 months with monthly rent of $1,500 due on the 1st of each month;\n"
            "•Security deposit of $1,500 held in escrow;\n"
            "•Tenant responsible for routine maintenance;\n"
            "•No subletting without landlord consent."
        )
    elif doc_type_val == "Employment Contract":
        current_parties = "John Doe (Employee), Apex Innovations Inc. (Employer)"
        current_terms = (
            "•Role of Senior Engineer reporting to CTO;\n"
            "•Annual compensation of $120,000 paid monthly;\n"
            "•Standard health insurance and 20 days paid annual leave;\n"
            "•Confidentiality and IP assignment to Employer."
        )

    # Parties Involved Textarea
    parties_val = st.text_area(
        "Parties Involved *",
        value=current_parties,
        height=90,
        placeholder="Party A (Role), Party B (Role)",
    )
    st.markdown(f'<div class="char-counter">{len(parties_val)}/500</div>', unsafe_allow_html=True)

    # Terms & Conditions Textarea
    terms_val = st.text_area(
        "Terms & Conditions *",
        value=current_terms,
        height=140,
        placeholder="Use semicolons for bullet points: Payment within 30 days; Confidentiality must be maintained;",
    )
    st.markdown(f'<div class="char-counter">{len(terms_val)}/2000</div>', unsafe_allow_html=True)

    # Effective Date
    dates_val = st.text_input("Effective Date *", value=DEFAULT_DATE)

    # Document Language
    lang_val = st.selectbox("Document Language *", ["English", "Hindi", "Tamil", "Spanish", "French"], index=0)

    st.write("")
    
    # Generate Document Button
    generate_clicked = st.button("🪄 Generate Document", type="primary", use_container_width=True)

    if generate_clicked:
        if not parties_val.strip() or not terms_val.strip() or not dates_val.strip():
            st.error("Please fill in all required fields marked with *.")
        else:
            with st.spinner("Drafting professional legal document..."):
                doc_text = None
                # First try FastAPI backend if running
                try:
                    payload = {
                        "document_type": doc_type_val,
                        "parties": parties_val,
                        "terms": terms_val,
                        "dates": dates_val,
                        "language": lang_val,
                        "api_key": api_key_input if not st.session_state["demo_mode"] else None,
                        "model": selected_model,
                    }
                    resp = requests.post(f"{BACKEND_URL}/generate", json=payload, timeout=25)
                    if resp.status_code == 200:
                        doc_text = resp.json().get("document", "")
                except Exception:
                    pass

                # If backend is not running or returned empty, generate directly via ai_core
                if not doc_text:
                    doc_text = generator.generate_document(
                        document_type=doc_type_val,
                        parties=parties_val,
                        terms=terms_val,
                        dates=dates_val,
                        language=lang_val,
                        api_key=api_key_input if not st.session_state["demo_mode"] else None,
                        model=selected_model,
                    )

                st.session_state["generated_doc"] = doc_text
                st.session_state["doc_type"] = doc_type_val
                st.session_state["edit_mode"] = False
                st.rerun()

# ---------------------------------------------------------
# RIGHT COLUMN (PREVIEW, ACTIONS, DOWNLOADS)
# ---------------------------------------------------------
with col_right:
    # If no document generated yet, generate initial sample preview
    if st.session_state["generated_doc"] is None:
        st.session_state["generated_doc"] = generator.generate_document(
            document_type=doc_type_val,
            parties=parties_val,
            terms=terms_val,
            dates=dates_val,
            language=lang_val,
        )

    # Success Alert Banner
    st.markdown(
        """
        <div class="success-alert">
            <span>✅</span>
            <span>Document Generated Successfully!</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    doc_content = st.session_state["generated_doc"]
    active_doc_type = st.session_state.get("doc_type", "Legal Document")

    # Action Buttons: Edit, Download TXT, Download DOCX, Download PDF
    btn_col1, btn_col2, btn_col3, btn_col4 = st.columns([1, 1.2, 1.3, 1.2])

    with btn_col1:
        edit_clicked = st.button("✏️ Edit", use_container_width=True)
        if edit_clicked:
            st.session_state["edit_mode"] = not st.session_state["edit_mode"]
            st.rerun()

    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in active_doc_type.lower()).strip("_")
    if not safe_name:
        safe_name = "legal_document"

    with btn_col2:
        txt_bytes_data = text_bytes(doc_content)
        st.download_button(
            label="📄 TXT",
            data=txt_bytes_data,
            file_name=f"{safe_name}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with btn_col3:
        docx_bytes_data = format_docx(doc_content, active_doc_type)
        st.download_button(
            label="📗 DOCX",
            data=docx_bytes_data,
            file_name=f"{safe_name}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )

    with btn_col4:
        pdf_bytes_data = format_pdf(doc_content, active_doc_type)
        st.download_button(
            label="📕 PDF",
            data=pdf_bytes_data,
            file_name=f"{safe_name}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    # Document Editor or Formatted Sheet
    if st.session_state.get("edit_mode", False):
        st.info("✏️ Edit mode is active. Modify the text below and your changes will reflect in downloads:")
        edited_text = st.text_area("Edit Document", value=doc_content, height=450, key="editor_area")
        if edited_text != doc_content:
            st.session_state["generated_doc"] = edited_text
    else:
        preview_html = format_html_preview(doc_content)
        st.markdown(f'<div class="document-paper">{preview_html}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# BOTTOM FEATURES FOOTER
# ---------------------------------------------------------
st.markdown(
    """
    <div class="footer-features">
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div>
                <p class="feature-title">Fast & Easy</p>
                <p class="feature-desc">Generate in seconds</p>
            </div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🛡️</div>
            <div>
                <p class="feature-title">Secure</p>
                <p class="feature-desc">Your data is protected</p>
            </div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">&lt;/&gt;</div>
            <div>
                <p class="feature-title">Multiple Formats</p>
                <p class="feature-desc">TXT, DOCX & PDF</p>
            </div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">✨</div>
            <div>
                <p class="feature-title">AI-Powered</p>
                <p class="feature-desc">Smart & accurate</p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)