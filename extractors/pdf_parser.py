import fitz  # PyMuPDF

def extract_all_pdf_text(pdf_path: str) -> str:
    """Extract the full text from a PDF using PyMuPDF."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text() + "\n"
    return text
