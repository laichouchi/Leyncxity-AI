import os
import PyPDF2
from docx import Document

def read_text_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading text file: {e}"

def read_pdf_file(path):
    try:
        text = ""
        with open(path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

def read_docx_file(path):
    try:
        doc = Document(path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        return f"Error reading Docx: {e}"

def get_file_content(path):
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        return "File not found."
    
    ext = os.path.splitext(path)[1].lower()
    if ext == '.txt':
        return read_text_file(path)
    elif ext == '.pdf':
        return read_pdf_file(path)
    elif ext in ['.docx', '.doc']:
        return read_docx_file(path)
    else:
        return "Unsupported file format for reading. Currently I support .txt, .pdf, and .docx."
