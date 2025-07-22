# app/utils.py

import fitz  # PyMuPDF

def extract_text_per_page(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []
    for i, page in enumerate(doc):
        pages.append((i + 1, page.get_text()))
    return pages
