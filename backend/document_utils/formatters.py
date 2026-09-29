import html
import re
from io import BytesIO
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import (
    WD_CELL_VERTICAL_ALIGNMENT,
    WD_TABLE_ALIGNMENT,
)
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

from fpdf import FPDF


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(
    __file__
).resolve().parents[2]

LOGO_PATH = (
    PROJECT_ROOT
    / "assets"
    / "logo.png"
)


# ---------------------------------------------------------
# SANITIZE TEXT
# ---------------------------------------------------------

def sanitize_text(text: str) -> str:

    if not text:
        return ""

    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
        "\u00a0": " ",
        "\u2022": "-",
    }

    for old, new in replacements.items():

        text = text.replace(
            old,
            new,
        )

    # Remove unsafe control characters.
    text = "".join(
        char
        for char in text
        if char in "\n\r\t"
        or ord(char) >= 32
    )

    return text.strip()


# ---------------------------------------------------------
# HTML PREVIEW
# ---------------------------------------------------------

def format_html_preview(text: str) -> str:

    safe_text = html.escape(
        sanitize_text(text)
    )

    lines = safe_text.splitlines()

    rendered = []

    for line in lines:

        stripped = line.strip()

        if not stripped:

            rendered.append(
                "<div class='spacer'></div>"
            )

        elif stripped.startswith("### "):

            rendered.append(
                f"<h3>{stripped[4:]}</h3>"
            )

        elif stripped.startswith("## "):

            rendered.append(
                f"<h2>{stripped[3:]}</h2>"
            )

        elif stripped.startswith("# "):

            rendered.append(
                f"<h1>{stripped[2:]}</h1>"
            )

        elif stripped.startswith("- "):

            rendered.append(
                f"<li>{stripped[2:]}</li>"
            )

        elif (
            stripped.startswith("**")
            and stripped.endswith("**")
        ):

            rendered.append(
                f"<p><strong>"
                f"{stripped[2:-2]}"
                f"</strong></p>"
            )

        else:

            # Basic bold support.
            formatted = re.sub(
                r"\*\*(.*?)\*\*",
                r"<strong>\1</strong>",
                stripped,
            )

            rendered.append(
                f"<p>{formatted}</p>"
            )

    return "".join(rendered)


# ---------------------------------------------------------
# DOCX HELPERS
# ---------------------------------------------------------

def set_cell_text(
    cell,
    text,
    bold=False,
):
    """
    Helper for writing formatted table cells.
    """

    cell.text = ""

    paragraph = cell.paragraphs[0]

    run = paragraph.add_run(
        text
    )

    run.bold = bold
    run.font.name = "Times New Roman"
    run.font.size = Pt(10)

    cell.vertical_alignment = (
        WD_CELL_VERTICAL_ALIGNMENT.CENTER
    )


def set_cell_shading(
    cell,
    fill="EAEAEA",
):

    tc_pr = cell._tc.get_or_add_tcPr()

    shd = OxmlElement("w:shd")

    shd.set(
        qn("w:fill"),
        fill,
    )

    tc_pr.append(shd)


# ---------------------------------------------------------
# DOCX FORMATTER
# ---------------------------------------------------------

def format_docx(
    text: str,
    doc_type: str,
) -> bytes:

    document = Document()

    section = document.sections[0]

    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

    # -----------------------------------------------------
    # DEFAULT FONT
    # -----------------------------------------------------

    normal_style = document.styles["Normal"]

    normal_style.font.name = (
        "Times New Roman"
    )

    normal_style.font.size = Pt(11)

    # -----------------------------------------------------
    # HEADER
    # -----------------------------------------------------

    header = section.header

    header_paragraph = (
        header.paragraphs[0]
    )

    header_paragraph.alignment = (
        WD_ALIGN_PARAGRAPH.CENTER
    )

    if LOGO_PATH.exists() and LOGO_PATH.stat().st_size > 0:
        try:
            run = (
                header_paragraph.add_run()
            )

            run.add_picture(
                str(LOGO_PATH),
                width=Inches(1.5),
            )
        except Exception:
            pass

    # -----------------------------------------------------
    # FOOTER
    # -----------------------------------------------------

    footer = section.footer

    footer_paragraph = (
        footer.paragraphs[0]
    )

    footer_paragraph.alignment = (
        WD_ALIGN_PARAGRAPH.CENTER
    )

    footer_run = (
        footer_paragraph.add_run(
            "LegalEase Inc. | contact@legalease.com | All Rights Reserved."
        )
    )

    footer_run.italic = True
    footer_run.font.name = (
        "Times New Roman"
    )
    footer_run.font.size = Pt(8)

    # -----------------------------------------------------
    # DOCUMENT TITLE
    # -----------------------------------------------------

    title_paragraph = (
        document.add_paragraph()
    )

    title_paragraph.alignment = (
        WD_ALIGN_PARAGRAPH.CENTER
    )

    title_run = (
        title_paragraph.add_run(
            sanitize_text(doc_type)
        )
    )

    title_run.bold = True
    title_run.font.name = (
        "Times New Roman"
    )
    title_run.font.size = Pt(16)

    # -----------------------------------------------------
    # CONTENT
    # -----------------------------------------------------

    terms = []

    clean_text = sanitize_text(text)

    for raw_line in clean_text.splitlines():

        line = raw_line.strip()

        if not line:
            continue

        # Collect bullet terms.
        if line.startswith("- "):

            terms.append(
                line[2:].strip()
            )

        # H1
        if line.startswith("# "):

            continue

        # H2
        if line.startswith("## "):

            paragraph = (
                document.add_paragraph()
            )

            run = paragraph.add_run(
                line[3:]
            )

            run.bold = True
            run.font.name = (
                "Times New Roman"
            )
            run.font.size = Pt(13)

            continue

        # H3
        if line.startswith("### "):

            paragraph = (
                document.add_paragraph()
            )

            run = paragraph.add_run(
                line[4:]
            )

            run.bold = True
            run.font.name = (
                "Times New Roman"
            )
            run.font.size = Pt(12)

            continue

        # Bullet
        if line.startswith("- "):

            paragraph = (
                document.add_paragraph(
                    style="List Bullet"
                )
            )

            run = paragraph.add_run(
                line[2:]
            )

            run.font.name = (
                "Times New Roman"
            )

            run.font.size = Pt(11)

            continue

        # Bold-only line
        if (
            line.startswith("**")
            and line.endswith("**")
        ):

            paragraph = (
                document.add_paragraph()
            )

            run = paragraph.add_run(
                line[2:-2]
            )

            run.bold = True
            run.font.name = (
                "Times New Roman"
            )

            continue

        # Normal paragraph
        paragraph = (
            document.add_paragraph()
        )

        # Basic Markdown bold conversion.
        parts = re.split(
            r"(\*\*.*?\*\*)",
            line,
        )

        for part in parts:

            if (
                part.startswith("**")
                and part.endswith("**")
            ):

                run = paragraph.add_run(
                    part[2:-2]
                )

                run.bold = True

            else:

                run = paragraph.add_run(
                    part
                )

            run.font.name = (
                "Times New Roman"
            )

            run.font.size = Pt(11)

    # -----------------------------------------------------
    # TERMS TABLE
    # -----------------------------------------------------

    if terms:

        document.add_paragraph()

        heading = (
            document.add_paragraph()
        )

        heading_run = (
            heading.add_run(
                "TERMS SUMMARY"
            )
        )

        heading_run.bold = True
        heading_run.font.name = (
            "Times New Roman"
        )
        heading_run.font.size = Pt(12)

        table = document.add_table(
            rows=1,
            cols=2,
        )

        table.style = "Table Grid"

        table.alignment = (
            WD_TABLE_ALIGNMENT.CENTER
        )

        header_cells = (
            table.rows[0].cells
        )

        set_cell_text(
            header_cells[0],
            "No.",
            bold=True,
        )

        set_cell_text(
            header_cells[1],
            "Term",
            bold=True,
        )

        set_cell_shading(
            header_cells[0]
        )

        set_cell_shading(
            header_cells[1]
        )

        for index, term in enumerate(
            terms,
            start=1,
        ):

            cells = (
                table.add_row().cells
            )

            set_cell_text(
                cells[0],
                str(index),
            )

            set_cell_text(
                cells[1],
                term,
            )

    # -----------------------------------------------------
    # SAVE TO MEMORY
    # -----------------------------------------------------

    output = BytesIO()

    document.save(output)

    return output.getvalue()


# ---------------------------------------------------------
# PDF CLASS
# ---------------------------------------------------------

class LegalEasePDF(FPDF):

    def __init__(
        self,
        title: str,
    ):

        super().__init__()

        self.doc_title = title

    # -----------------------------------------------------
    # HEADER
    # -----------------------------------------------------

    def header(self):

        if LOGO_PATH.exists() and LOGO_PATH.stat().st_size > 0:

            try:

                self.image(
                    str(LOGO_PATH),
                    x=80,
                    y=8,
                    w=50,
                )

                self.ln(17)

            except Exception:

                self.set_font(
                    "Helvetica",
                    "B",
                    12,
                )

                self.cell(
                    0,
                    8,
                    "LegalEase",
                    align="C",
                )

                self.ln(10)

        else:

            self.set_font(
                "Helvetica",
                "B",
                12,
            )

            self.cell(
                0,
                8,
                "LegalEase",
                align="C",
            )

            self.ln(10)

        self.set_font(
            "Helvetica",
            "B",
            10,
        )

        self.cell(
            0,
            7,
            self.doc_title[:90],
            align="C",
        )

        self.ln(8)

        self.line(
            12,
            self.get_y(),
            198,
            self.get_y(),
        )

        self.ln(5)

    # -----------------------------------------------------
    # FOOTER
    # -----------------------------------------------------

    def footer(self):

        self.set_y(-15)

        self.set_font(
            "Helvetica",
            "I",
            8,
        )

        self.cell(
            0,
            8,
            "LegalEase Inc. | contact@legalease.com | All Rights Reserved.",
            align="C",
        )


# ---------------------------------------------------------
# PDF FORMATTER
# ---------------------------------------------------------

def format_pdf(
    text: str,
    doc_type: str,
) -> bytes:

    pdf = LegalEasePDF(
        doc_type
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=20,
    )

    pdf.set_margins(
        18,
        20,
        18,
    )

    pdf.add_page()

    clean_text = sanitize_text(text).encode("latin-1", "replace").decode("latin-1")

    for raw_line in clean_text.splitlines():
        line = raw_line.strip()
        if not line:
            pdf.ln(3)
            continue

        # H1
        if line.startswith("# "):
            pdf.set_font("Helvetica", "B", 14)
            pdf.multi_cell(0, 8, line[2:])
            pdf.ln(2)

        # H2
        elif line.startswith("## "):
            pdf.set_font("Helvetica", "B", 12)
            pdf.multi_cell(0, 7, line[3:])
            pdf.ln(1)

        # H3
        elif line.startswith("### "):
            pdf.set_font("Helvetica", "B", 11)
            pdf.multi_cell(0, 6, line[4:])

        # Bullet
        elif line.startswith("- "):
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(0, 5.5, "- " + line[2:])

        # Normal paragraph
        else:
            paragraph = line.replace("**", "").replace("*", "")
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(0, 5.5, paragraph)

    out = pdf.output(dest="S")
    if isinstance(out, str):
        return out.encode("latin-1", "replace")
    return bytes(out)


# ---------------------------------------------------------
# TXT FORMATTER
# ---------------------------------------------------------

def text_bytes(
    text: str,
) -> bytes:

    return sanitize_text(
        text
    ).encode(
        "utf-8"
    )