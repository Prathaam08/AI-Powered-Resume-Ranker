import os
import re
from pdfminer.high_level import extract_text as pdfminer_extract_text
from docx import Document
import logging

logger = logging.getLogger(__name__)

def extract_text(file_path):
    try:
        if file_path.endswith('.pdf'):
            return extract_pdf_text(file_path)
        elif file_path.endswith('.docx'):
            return extract_docx_text(file_path)
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception as e:
        logger.error(f"Error extracting text from {file_path}: {str(e)}")
        return ""

def extract_pdf_text(file_path):
    try:
        return pdfminer_extract_text(file_path)
    except Exception as e:
        logger.error(f"Error extracting PDF text from {file_path}: {str(e)}")
        return ""

def extract_docx_text(file_path):
    try:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        logger.error(f"Error extracting DOCX text from {file_path}: {str(e)}")
        return ""

def extract_contact_info(text):
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    phone_pattern = r'(\+?\d{1,3}[\s.-]?)?(\(?\d{2,4}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{4}'

    email = re.search(email_pattern, text)
    phone = re.search(phone_pattern, text)

    return {
        'email': email.group(0) if email else '',
        'phone': phone.group(0) if phone else ''
    }
