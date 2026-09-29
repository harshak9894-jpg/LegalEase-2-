import os
import re
import warnings
from textwrap import dedent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try modern google.genai SDK first, then legacy google.generativeai
try:
    from google import genai
except ImportError:
    genai = None

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        import google.generativeai as legacy_genai
    except ImportError:
        legacy_genai = None

DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")


class GeminiDocumentGenerator:
    """
    AI Legal Document Generator using Google Gemini.
    Compliant with the SmartBridge / SmartInternz LegalEase specification.
    Supports both Gemini 3.8/2.5/1.5 models and intelligent fallback.
    """

    def __init__(self, model_name: str = None):
        self._load_config()
        if model_name:
            self.model_name = model_name

    def _load_config(self):
        load_dotenv(override=True)
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model_name = os.getenv("GEMINI_MODEL", DEFAULT_MODEL).strip()
        self.demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str,
        language: str = "English",
        api_key: str = None,
        model: str = None,
    ) -> str:
        """
        Generates a structured legal document based on input parameters.
        Returns document text as specified in Activity 2.1 & 3.2 of the faculty PDF.
        """
        self._load_config()
        active_key = (api_key or self.api_key or "").strip()
        active_model = (model or self.model_name or DEFAULT_MODEL).strip()

        # If explicitly in demo mode or no API key configured
        if self.demo_mode or not active_key:
            return self._build_template_document(
                document_type=document_type,
                parties=parties,
                terms=terms,
                dates=dates,
                language=language,
            )

        prompt = self._build_prompt(
            document_type=document_type,
            parties=parties,
            terms=terms,
            dates=dates,
            language=language,
        )

        # 1. Try modern google.genai client if available
        if genai is not None:
            try:
                client = genai.Client(api_key=active_key)
                response = client.models.generate_content(
                    model=active_model,
                    contents=prompt,
                )
                if response and hasattr(response, "text") and response.text:
                    return response.text.strip()
            except Exception:
                pass

        # 2. Try legacy google.generativeai (which works reliably in this environment)
        if legacy_genai is not None:
            try:
                legacy_genai.configure(api_key=active_key)
                # Try requested model
                model_inst = legacy_genai.GenerativeModel(active_model)
                response = model_inst.generate_content(prompt)
                if response and hasattr(response, "text") and response.text:
                    return response.text.strip()
            except Exception as exc:
                # If error is 404 model not found, try gemini-3.8-flash as fallback
                if "404" in str(exc) and active_model != "gemini-3.8-flash":
                    try:
                        fallback_model = legacy_genai.GenerativeModel("gemini-3.8-flash")
                        resp = fallback_model.generate_content(prompt)
                        if resp and hasattr(resp, "text") and resp.text:
                            return resp.text.strip()
                    except Exception:
                        pass

        # 3. If API quota is exceeded (429) or offline, seamlessly return structured template
        return self._build_template_document(
            document_type=document_type,
            parties=parties,
            terms=terms,
            dates=dates,
            language=language,
        )

    @staticmethod
    def _build_prompt(document_type: str, parties: str, terms: str, dates: str, language: str) -> str:
        return dedent(
            f"""
            Generate a comprehensive legal document titled '{document_type}'
            Involved parties: {parties}
            Effective Date: {dates}
            Terms and conditions: {terms}
            Ensure formal legal structure with multiple sections and legal clauses.
            Output Language: {language}

            Requirements:
            - Professional legal preamble with 'Between:', 'And:', 'WITNESSETH:', 'WHEREAS...'
            - Formal recitals and 'NOW, THEREFORE...'
            - Numbered legal sections integrating the terms and conditions with full clarity
            - Clauses for Confidentiality, Governing Law, Entire Agreement, and Severability
            - Formal signature lines for each party with name, title, and date
            - Format cleanly with Markdown headings (##) and bullet points (- )
            - Return only the legal document text
            """
        ).strip()

    @staticmethod
    def _build_template_document(
        document_type: str,
        parties: str,
        terms: str,
        dates: str,
        language: str = "English",
    ) -> str:
        party_lines = [p.strip() for p in re.split(r",|\n| and |;| vs | & ", parties, flags=re.IGNORECASE) if p.strip()]
        p1 = party_lines[0] if len(party_lines) > 0 else "First Party"
        p2 = party_lines[1] if len(party_lines) > 1 else "Second Party"

        term_items = [t.strip() for t in terms.split(";") if t.strip()]
        if not term_items:
            term_items = [
                "The parties agree to perform all obligations in good faith.",
                "Payment shall be made within thirty (30) days of invoice receipt.",
                "Confidentiality must be strictly maintained at all times.",
                "Either party may terminate this agreement with fifteen (15) days written notice.",
            ]

        formatted_terms = "\n".join([f"{i+1}. {t}" for i, t in enumerate(term_items)])

        doc = dedent(
            f"""
            ## {document_type.upper()}

            This {document_type} ("Agreement") is made on {dates}, between:

            **1. Service Provider / First Party:**
            - **Name:** {p1}
            - **Address:** Primary Registered Office / Residence

            **2. Client / Second Party:**
            - **Name:** {p2}
            - **Address:** Principal Place of Business

            **3. PURPOSE**
            The purpose of this agreement is to define the terms and conditions under which the services, responsibilities, and mutual obligations will be executed between {p1} and {p2}.

            **4. TERMS AND CONDITIONS**
            {formatted_terms}

            **5. GENERAL PROVISIONS**
            - **Confidentiality:** All proprietary information shared under this Agreement shall remain strictly confidential.
            - **Governing Law:** This agreement shall be governed by and construed in accordance with applicable laws.
            - **Severability:** In the event that any provision is found unenforceable, all other clauses remain valid and binding.
            - **Entire Agreement:** This constitutes the entire agreement and supersedes any prior oral or written discussions.

            **6. SIGNATURES**

            _______________________________________                _______________________________________
            **{p1}**                                              **{p2}**
            Authorized Signatory                                   Authorized Signatory
            Date: {dates}                                          Date: {dates}
            """
        ).strip()
        return doc
