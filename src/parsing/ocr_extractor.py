import os
import cv2
import logging
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from datetime import datetime
from utils.logger import logging as logger

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
POPPLER_PATH = r'C:\poppler\poppler\Library\bin'

def preprocess_image(img):
    """Applies Grayscale and Thresholding to improve OCR."""
    import numpy as np
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return Image.fromarray(thresh)

def process_ocr(image, source_name):
    """Runs OCR on both raw and preprocessed images and compares them."""
    try:
        raw_text = pytesseract.image_to_string(image)
        
        processed_img = preprocess_image(image)
        optimized_text = pytesseract.image_to_string(processed_img)
        
        logger.info(f"OCR Compare [{source_name}]: Raw ({len(raw_text)} chars) vs Optimized ({len(optimized_text)} chars)")
        
        return {
            "file_name": source_name,
            "source": "Local OCR",
            "type": "OCR Data",
            "timestamp": datetime.now().isoformat(),
            "raw_ocr_content": raw_text.strip(),
            "optimized_ocr_content": optimized_text.strip()
        }
    except Exception as e:
        logger.error(f"OCR processing failed for {source_name}: {e}")
        return None

def extract_text_from_image(file_path):
    logger.info(f"Starting OCR for image: {file_path}")
    img = Image.open(file_path)
    return process_ocr(img, os.path.basename(file_path))

def extract_text_from_scanned_pdf(pdf_path):
    """Uses pdf2image and poppler to read scanned PDFs."""
    logger.info(f"Starting OCR for scanned PDF: {pdf_path}")
    extracted_pages = []
    try:
        pages = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
        for i, page_img in enumerate(pages):
            logger.info(f"Running OCR on page {i+1} of {os.path.basename(pdf_path)}")
            data = process_ocr(page_img, f"{os.path.basename(pdf_path)} - Page {i+1}")
            if data:
                extracted_pages.append(data)
    except Exception as e:
        logger.error(f"Failed to process scanned PDF {pdf_path}: {e}")
    return extracted_pages