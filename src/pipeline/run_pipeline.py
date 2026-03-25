'''import sys
import os

# Ensure Python finds your 'src' folders per lab instructions
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.logger import logging
from api.client import fetch_loopnet_data
from parsing.parsers import parse_loopnet_map_data
from storage.mongo import save_to_mongo
from storage.s3 import upload_file_to_s3

def run_pipeline():
    logging.info("Starting Real Estate Market Monitor Pipeline...")

    # 1. Fetch live data (Pages=3)
    logging.info("Fetching data from API...")
    raw_properties = fetch_loopnet_data(pages=3)

    if not raw_properties:
        logging.error("No data fetched from API. Pipeline stopping.")
        return

    # 2. Parse and Save to MongoDB
    logging.info("Parsing data...")
    cleaned_properties = [parse_loopnet_map_data(item) for item in raw_properties] # <-- Changed this
    
    logging.info("Saving to MongoDB...")
    save_to_mongo(cleaned_properties, "loopnet_listings")

    # 3. Upload raw pages to S3
    logging.info("Uploading raw files to S3...")
    for page in range(1, 4):
        file_name = f"loopnet_page_{page}.json"
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f"../../data/raw/api/{file_name}"))
        upload_file_to_s3(file_path, file_name)

    logging.info("Pipeline finished successfully")

if __name__ == "__main__":
    run_pipeline()'''

import sys
import os

# Ensure Python finds your 'src' folders per lab instructions
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.logger import logging
from api.client import fetch_loopnet_data
from parsing.parsers import parse_loopnet_map_data
from storage.mongo import save_to_mongo
from storage.s3 import upload_file_to_s3
from parsing.document_extractors import extract_from_pdf, extract_from_word, extract_from_excel

def run_pipeline():
    logging.info("Starting Real Estate Market Monitor Pipeline...")
    print("🚀 Starting Pipeline...")

    # =================================================================
    # PHASE 1: PREVIOUS LAB FUNCTIONALITY (API -> Mongo -> S3)
    # =================================================================
    logging.info("Fetching data from API...")
    print("🌐 Running Phase 1: API Fetching...")
    raw_properties = fetch_loopnet_data(pages=3)

    if not raw_properties:
        logging.error("No data fetched from API. Skipping API storage steps.")
        print("⚠️ No API data fetched. Moving to Phase 2.")
    else:
        # 2. Parse and Save to MongoDB
        logging.info("Parsing data...")
        cleaned_properties = [parse_loopnet_map_data(item) for item in raw_properties] 
        
        logging.info("Saving to MongoDB...")
        save_to_mongo(cleaned_properties, "loopnet_listings")

        # 3. Upload raw pages to S3
        # logging.info("Uploading raw files to S3...")
        #for page in range(1, 4):
         #   file_name = f"loopnet_page_{page}.json"
          #  file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f"../../data/raw/api/{file_name}"))
         #   upload_file_to_s3(file_path, file_name) 

    # =================================================================
    # PHASE 2: NEW LAB FUNCTIONALITY (Document Extraction -> Mongo)
    # =================================================================
    logging.info("Starting unstructured document extraction...")
    print("📂 Running Phase 2: Document Extraction...")
    
    all_document_data = []
    
    # Establish dynamic paths based on your folder structure
    base_raw_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), f"../../data/raw"))
    pdf_dir = os.path.join(base_raw_dir, "pdf")
    word_dir = os.path.join(base_raw_dir, "word")
    excel_dir = os.path.join(base_raw_dir, "excell") # Using your exact folder spelling
    
    # Process PDFs
    if os.path.exists(pdf_dir):
        for filename in os.listdir(pdf_dir):
            if filename.lower().endswith(".pdf"):
                path = os.path.join(pdf_dir, filename)
                all_document_data.extend(extract_from_pdf(path))
                
    # Process Word
    if os.path.exists(word_dir):
        for filename in os.listdir(word_dir):
            if filename.lower().endswith(".docx"):
                path = os.path.join(word_dir, filename)
                all_document_data.extend(extract_from_word(path))
                
    # Process Excel
    if os.path.exists(excel_dir):
        for filename in os.listdir(excel_dir):
            if filename.lower().endswith(".xlsx"):
                path = os.path.join(excel_dir, filename)
                all_document_data.extend(extract_from_excel(path))

    # Save documents to MongoDB
    if all_document_data:
        logging.info(f"Saving {len(all_document_data)} document records to MongoDB...")
        save_to_mongo(all_document_data, "extracted_documents")
        print(f"✅ Extracted and saved {len(all_document_data)} document records to MongoDB.")
    else:
        logging.warning("No documents found in raw directories to extract.")
        print("⚠️ No documents extracted (folders are empty).")

    logging.info("Pipeline finished successfully")
    print("🏁 Pipeline finished successfully!")

if __name__ == "__main__":
    run_pipeline()