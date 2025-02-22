# file_parser.py

import fitz  # PyMuPDF
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
        return _extract_text_from_pdf(file_path)
    elif suffix == ".docx":
        return _extract_text_from_docx(file_path)
    elif suffix in [".html", ".htm"]:
        return _extract_text_from_html(file_path)
    else:  # txt or other text formats
        return _extract_text_from_txt(file_path)

def _extract_text_from_pdf(file_path: Path) -> str:
    """
    Extract text from PDF using PyMuPDF (fitz).
    """
    doc = fitz.open(file_path)
    text = []
    for page in doc:
        text.append(page.get_text())
    return "\n".join(text)

def _extract_text_from_docx(file_path: Path) -> str:
    """
    Extract text from a DOCX file using python-docx.
    """
    doc = Document(file_path)
    # Join all paragraphs with line breaks
    return "\n".join(p.text for p in doc.paragraphs)

def _extract_text_from_html(file_path: Path) -> str:
    """
    Extract text from an HTML file using BeautifulSoup.
    """
    with file_path.open('r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        return soup.get_text()

def _extract_text_from_txt(file_path: Path) -> str:
    """
    Extract text from a plain text file or unsupported extension,
    falling back to reading it as .txt.
    """
    with file_path.open('r', encoding='utf-8', errors='ignore') as f:
        return f.read()