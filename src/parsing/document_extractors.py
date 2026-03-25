import os
import logging
from datetime import datetime
import pdfplumber
import docx
import openpyxl
import chardet
import os

def safe_decode(raw_text):
    """Uses chardet to detect and safely decode text to handle encoding issues."""
    if not raw_text:
        return ""
    
    # Convert to bytes to satisfy the chardet requirement
    raw_bytes = raw_text.encode('utf-8') if isinstance(raw_text, str) else raw_text
    
    # 1. Ask chardet to guess the encoding
    detection = chardet.detect(raw_bytes)
    encoding = detection.get('encoding', 'utf-8') or 'utf-8'
    
    try:
        return raw_bytes.decode(encoding)
    except Exception:
        fallbacks = ['utf-8', 'cp1252', 'latin-1']
        for fb in fallbacks:
            try:
                return raw_bytes.decode(fb)
            except Exception:
                continue
                
        # 4. If all decodings fail, use 'replace' instead of 'ignore'
        # This guarantees the text is processed without dropping any parts of the file
        return raw_bytes.decode('utf-8', errors='replace')      
        
def get_base_metadata(file_path, doc_type, library):
    """Generates the required standardized metadata for documents."""
    return {
        "file_name": os.path.basename(file_path),
        "document_type": doc_type,
        "extraction_timestamp": datetime.now().isoformat(),
        "source": "Local Storage",
        "extraction_library": library
    }

def extract_from_pdf(file_path):
    logging.info(f"Extracting PDF: {file_path}")
    extracted_data = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                safe_text = safe_decode(text)
                
                record = get_base_metadata(file_path, "PDF", "pdfplumber")
                record["page_number"] = i + 1
                record["content"] = safe_text.strip()
                extracted_data.append(record)
    except Exception as e:
        logging.error(f"Failed to process PDF {file_path}: {e}")
    return extracted_data

def extract_from_word(file_path):
    logging.info(f"Extracting Word Document: {file_path}")
    extracted_data = []
    try:
        doc = docx.Document(file_path)
        full_text = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
        
        raw_text = "\n".join(full_text)
        safe_text = safe_decode(raw_text)
        
        record = get_base_metadata(file_path, "Word", "python-docx")
        record["content"] = safe_text
        extracted_data.append(record)
    except Exception as e:
        logging.error(f"Failed to process Word {file_path}: {e}")
    return extracted_data

def extract_from_excel(file_path):
    logging.info(f"Extracting Excel Document: {file_path}")
    extracted_data = []
    try:
        wb = openpyxl.load_workbook(file_path, data_only=True)
        for sheet_name in wb.sheetnames:
            sheet = wb[sheet_name]
            sheet_content = []
            
            for row in sheet.iter_rows(values_only=True):
                clean_row = [str(cell) for cell in row if cell is not None]
                if clean_row:
                    sheet_content.append(" | ".join(clean_row))
            
            raw_text = "\n".join(sheet_content)
            safe_text = safe_decode(raw_text)
            
            record = get_base_metadata(file_path, "Excel", "openpyxl")
            record["sheet_name"] = sheet_name
            record["content"] = safe_text
            extracted_data.append(record)
    except Exception as e:
        logging.error(f"Failed to process Excel {file_path}: {e}")
    return extracted_data

