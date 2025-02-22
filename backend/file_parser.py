# file_parser.py
from pdfminer.high_level import extract_text  # Replace fitz with pdfminer
from docx import Document  # python-docx package
from bs4 import BeautifulSoup
from pathlib import Path

def parse_file(file_path: Path) -> str:
    """
    Parse text from a file, supported suffixes: .pdf, .docx, .html, .htm, .txt
    :param file_path: Path object to the file.
    :return: Extracted text as a string.
    """
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        return extract_text_from_pdf(file_path)
    elif suffix == ".docx":
        return extract_text_from_docx(file_path)
    elif suffix in [".html", ".htm"]:
        return extract_text_from_html(file_path)
    else:  # txt or other text formats
        return extract_text_from_txt(file_path)

def extract_text_from_pdf(file_path: Path) -> str:
    """
    Extract text from PDF using pdfminer.six.
    """
    # PDFMiner's extract_text handles file opening and text extraction
    return extract_text(str(file_path))

def extract_text_from_docx(file_path: Path) -> str:
    """
    Extract text from a DOCX file using python-docx.
    """
    doc = Document(file_path)
    # Join all paragraphs with line breaks
    return "\n".join(p.text for p in doc.paragraphs)

def extract_text_from_html(file_path: Path) -> str:
    """
    Extract text from an HTML file using BeautifulSoup.
    """
    with file_path.open('r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        return soup.get_text()

def extract_text_from_txt(file_path: Path) -> str:
    """
    Extract text from a plain text file or unsupported extension,
    falling back to reading it as .txt.
    """
    with file_path.open('r', encoding='utf-8', errors='ignore') as f:
        return f.read()