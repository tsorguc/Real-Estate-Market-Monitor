import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.logger import logging
from api.client import fetch_loopnet_data
from parsing.parsers import parse_loopnet_map_data
from storage.mongo import save_to_mongo
# from storage.s3 import upload_file_to_s3
from parsing.document_extractors import extract_from_pdf, extract_from_word, extract_from_excel
from scraping.scraper import scrape_static_pages, scrape_dynamic_page
from parsing.ocr_extractor import extract_text_from_image, extract_text_from_scanned_pdf

# New Imports for Image Processing
from image_processing.downloader import fetch_and_download_images
from image_processing.batch import batch_process_images
from utils.report_generator import generate_combined_report

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
        logging.warning("No data fetched from API. Checking for local raw data fallback...")
        base_raw_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), f"../../data/raw"))
        api_raw_dir = os.path.join(base_raw_dir, "api")
        if os.path.exists(api_raw_dir):
            for filename in os.listdir(api_raw_dir):
                if filename.endswith(".json"):
                    with open(os.path.join(api_raw_dir, filename), "r", encoding="utf-8") as f:
                        raw_properties.extend(json.load(f))
        
        if raw_properties:
            print(f"📦 Loaded {len(raw_properties)} items from local cache.")
        else:
            logging.error("No data fetched from API and no local cache found. Skipping API storage steps.")
            print("⚠️ No API data available. Moving to Phase 2.")

    if raw_properties:
        # 2. Parse and Save to MongoDB
        logging.info("Parsing data...")
        cleaned_properties = [parse_loopnet_map_data(item) for item in raw_properties] 
        
        logging.info("Saving to MongoDB...")
        save_to_mongo(cleaned_properties, "loopnet_listings")

        # =================================================================
        # NEW: PHASE 1.5 - IMAGE PROCESSING
        # =================================================================
        logging.info("Starting Phase 1.5: Image Processing...")
        print("🖼️ Running Phase 1.5: Image Processing...")
        
        # Download images from the fetched API data
        fetch_and_download_images(raw_properties)
        
        # Process the downloaded images
        raw_images_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/raw/property_images"))
        batch_process_images(raw_images_dir, raw_properties)
        
        print("✅ Image processing batch job completed.")

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

    # =================================================================
    # PHASE 3: LAB 5 - WEB SCRAPING
    # =================================================================
    logging.info("Starting Phase 3: Web Scraping...")
    print("🕸️ Running Phase 3: Web Scraping...")
    
    target_static_url = "http://books.toscrape.com/catalogue/category/books_1/index.html" 
    static_data = scrape_static_pages(target_static_url, max_pages=2)
    
    target_dynamic_url = "https://quotes.toscrape.com/scroll" 
    dynamic_data = scrape_dynamic_page(target_dynamic_url)
    
    combined_scraping_data = static_data + dynamic_data
    if combined_scraping_data:
        save_to_mongo(combined_scraping_data, "scraped_web_data")
        print(f"✅ Extracted and saved {len(combined_scraping_data)} scraped web items to MongoDB.")
    else:
        print("⚠️ No web data scraped.")

    # =================================================================
    # PHASE 4: LAB 5 - OCR Processing
    # =================================================================
    logging.info("Starting Phase 4: OCR Image Processing...")
    print("📸 Running Phase 4: OCR Extraction...")
    
    ocr_data_list = []
    img_dir = os.path.join(base_raw_dir, "img")
    
    if os.path.exists(img_dir):
        for filename in os.listdir(img_dir):
            file_path = os.path.join(img_dir, filename)

            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                extracted_data = extract_text_from_image(file_path)
                if extracted_data: ocr_data_list.append(extracted_data)
            elif filename.lower().endswith('.pdf'):
                extracted_pages = extract_text_from_scanned_pdf(file_path)
                ocr_data_list.extend(extracted_pages)

    if ocr_data_list:
        save_to_mongo(ocr_data_list, "ocr_extracted_data")
        print(f"✅ Extracted and saved {len(ocr_data_list)} OCR records to MongoDB.")
    else:
        logging.warning("No images found in data/raw/img for OCR extraction.")
        print("⚠️ No images found in data/raw/img for OCR extraction.")
    

    logging.info("Pipeline finished successfully")
    print("🏁 Pipeline finished successfully!")
    
    # Final step: Generate the summary report for the user
    generate_combined_report()

if __name__ == "__main__":
    run_pipeline()
