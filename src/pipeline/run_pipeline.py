import sys
import os
import json
import pandas as pd

# Add both 'src' and project root to sys.path to handle inconsistent import styles
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.utils.logger import logging
from src.api.client import fetch_loopnet_data
from src.parsing.parsers import parse_loopnet_map_data
from src.storage.mongo import save_to_mongo
# from src.storage.s3 import upload_file_to_s3
from src.parsing.document_extractors import extract_from_pdf, extract_from_word, extract_from_excel
from src.scraping.scraper import scrape_static_pages, scrape_dynamic_page
from src.parsing.ocr_extractor import extract_text_from_image, extract_text_from_scanned_pdf

# --- LAB 7 AUDIO/VIDEO EXTENSION ---
from src.audio_processing.loader import load_audio
from src.audio_processing.processor import trim_audio, concatenate_audio, adjust_volume, apply_fades, convert_audio
from src.audio_processing.transcriber import transcribe_audio, chunked_transcribe
from src.video_processing.loader import load_video_and_extract_audio
from src.video_processing.frame_extractor import extract_keyframes
from src.storage.mongo import save_transcript_to_mongo

# New Imports for Image Processing
from src.image_processing.downloader import fetch_and_download_images
from src.image_processing.batch import batch_process_images
from src.utils.report_generator import generate_combined_report

# New Imports for Analytics (Lab 8)
from src.analytics import (
    demonstrate_numpy_features,
    get_integrated_data,
    optimize_dataframe,
    export_to_csv,
    load_csv_in_chunks,
    process_chunks_per_category,
    perform_eda,
    demonstrate_selection,
    perform_regex_operations,
    generate_quality_report
)

# New Imports for Cleaning (Lab 9)
from src.cleaning import run_cleaning_pipeline

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
    
    # =================================================================
    # PHASE 5: LAB 7 - AUDIO/VIDEO PROCESSING
    # =================================================================
    logging.info("Starting Phase 5: Audio and Video Processing...")
    print("🎵 Running Phase 5: Audio/Video Processing...")

    audio_raw_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/raw/audio"))
    video_raw_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/raw/video"))
    audio_proc_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/processed/audio"))
    frames_proc_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/processed/frames"))
    transcripts_proc_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/processed/transcripts"))

    # 1. Process Audio Files
    audio_files = [f for f in os.listdir(audio_raw_dir) if f.lower().endswith(('.mp3', '.wav', '.flac', '.ogg'))] if os.path.exists(audio_raw_dir) else []
    
    if audio_files:
        loaded_clips = []
        for i, filename in enumerate(audio_files[:3]): # Load and inspect at least 3
            file_path = os.path.join(audio_raw_dir, filename)
            audio_clip = load_audio(file_path)
            if audio_clip:
                loaded_clips.append(audio_clip)
                
                if i == 0: # Demonstrate operations on the first clip
                    # Trim
                    trim_path = os.path.join(audio_proc_dir, "trimmed_sample.wav")
                    trim_audio(audio_clip, 0, 5000, trim_path)
                    
                    # Volume and Fades
                    modified = adjust_volume(audio_clip, gain_db=5)
                    modified = apply_fades(modified, fade_in_ms=1000, fade_out_ms=1000)
                    
                    # Convert
                    convert_path = os.path.join(audio_proc_dir, "converted_sample.ogg")
                    convert_audio(modified, convert_path)

        # Concatenate
        if len(loaded_clips) >= 2:
            concat_path = os.path.join(audio_proc_dir, "concatenated_sample.wav")
            concatenate_audio(loaded_clips[:2], concat_path)

        # Transcription
        for filename in audio_files[:1]:
            file_path = os.path.join(audio_raw_dir, filename)
            transcript_out = os.path.join(transcripts_proc_dir, os.path.splitext(filename)[0])
            
            # Short transcription
            result = transcribe_audio(file_path, output_base_path=transcript_out)
            if result:
                save_transcript_to_mongo(result, file_path, result["language"], "faster-whisper-base")
                print(f"✅ Transcribed {filename}")

            # Chunked transcription (demonstration on the same or another file)
            chunked_result = chunked_transcribe(file_path, output_dir=transcripts_proc_dir)
            if chunked_result:
                logging.info(f"Chunked transcription completed for {filename}")
    else:
        print("⚠️ No audio files found in data/raw/audio.")

    # 2. Process Video Files
    video_files = [f for f in os.listdir(video_raw_dir) if f.lower().endswith(('.mp4', '.mkv', '.mov', '.avi'))] if os.path.exists(video_raw_dir) else []
    
    if video_files:
        for filename in video_files[:1]:
            video_path = os.path.join(video_raw_dir, filename)
            extracted_audio_path = os.path.join(audio_proc_dir, f"{os.path.splitext(filename)[0]}_from_video.mp3")
            
            # Load and extract audio
            load_video_and_extract_audio(video_path, extracted_audio_path)
            
            # Extract keyframes
            extract_keyframes(video_path, frames_proc_dir, interval_seconds=10)
            
            # Transcribe extracted audio
            if os.path.exists(extracted_audio_path):
                transcript_out = os.path.join(transcripts_proc_dir, f"{os.path.splitext(filename)[0]}_video_transcript")
                result = transcribe_audio(extracted_audio_path, output_base_path=transcript_out)
                if result:
                    save_transcript_to_mongo(result, video_path, result["language"], "faster-whisper-base")
                    print(f"✅ Transcribed audio from video {filename}")
    else:
        print("⚠️ No video files found in data/raw/video.")

    # =================================================================
    # PHASE 6: LAB 8 - DATA ANALYTICS
    # =================================================================
    logging.info("Starting Phase 6: Data Analytics...")
    print("📊 Running Phase 6: Data Analytics...")

    # 1. NumPy Foundations
    numpy_results = demonstrate_numpy_features()
    print(f"✅ NumPy demonstration completed. Max Price: {numpy_results['max_price']}")

    # 2. Loading & Integration
    df = get_integrated_data()
    logging.info(f"Loaded integrated data with {len(df)} records.")
    
    # 3. Memory Optimization
    df = optimize_dataframe(df)
    
    # 4. Export and Chunked Loading
    raw_csv_path = export_to_csv(df, "raw_integrated_data.csv")
    global_mean = load_csv_in_chunks(raw_csv_path, chunk_size=20)
    print(f"📈 Global mean price from chunks: ${global_mean:,.2f}")
    
    # 5. Process chunks per-category
    category_means = process_chunks_per_category(raw_csv_path, chunk_size=20)
    print(f"🏘️ Category means computed from chunks: {list(category_means.keys())}")

    # 6. Exploratory Data Analysis
    perform_eda(df)
    print("📈 EDA completed and charts saved.")

    # 7. Selection & Filtering
    demonstrate_selection(df)
    print("🔍 Selection and filtering demonstration completed.")

    # 8. Regex Operations
    df = perform_regex_operations(df)
    print("🔡 Regex operations on text columns completed.")

    # 9. Data Quality Assessment
    generate_quality_report(df)
    print("🛠️ Data Quality Report generated.")

    # =================================================================
    # PHASE 7: LAB 9 - DATA CLEANING
    # =================================================================
    logging.info("Starting Phase 7: Data Cleaning...")
    print("🧹 Running Phase 7: Data Cleaning...")
    
    clean_df = run_cleaning_pipeline(df)
    print(f"✅ Data cleaning pipeline completed. Cleaned records: {len(clean_df)}")

    # =================================================================
    # PHASE 8: LAB 10 - ADVANCED ANALYTICS
    # =================================================================
    logging.info("Starting Phase 8: Advanced Analytics...")
    print("📈 Running Phase 8: Advanced Analytics...")

    from src.analytics import db_connector, data_combiner, aggregator, pivot_builder, time_series, insight_reporter, mongo_pipeline

    # 1. Ensure cleaned data exists
    cleaned_csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/processed/cleaned/cleaned_data.csv"))
    if not os.path.exists(cleaned_csv_path):
        logging.warning("Cleaned data file not found. Running cleaning pipeline...")
        clean_df = run_cleaning_pipeline(df) 
    else:
        clean_df = pd.read_csv(cleaned_csv_path)
    
    # 2. Populate and Query MySQL
    logging.info("Populating MySQL database...")
    db_connector.populate_financials(cleaned_csv_path)
    df_financials = db_connector.query_financials()
    
    # 3. Data Combination (Join Comparison)
    logging.info("Comparing join types...")
    data_combiner.compare_joins(df_financials, clean_df)
    
    # 4. Reshaping and Pivoting
    logging.info("Generating pivot tables...")
    pivot_table = pivot_builder.create_genre_year_pivot(df_financials)
    pivot_table.to_csv(os.path.join(os.path.dirname(__file__), "../../data/processed/analytics/pivot_genre_year.csv"))
    
    # 5. GroupBy Analysis
    logging.info("Performing GroupBy aggregations...")
    type_summary = aggregator.calculate_type_summary(df_financials)
    type_summary.to_csv(os.path.join(os.path.dirname(__file__), "../../data/processed/analytics/genre_analysis.csv"))
    
    yearly_trends = aggregator.calculate_yearly_trends(df_financials)
    yearly_trends.to_csv(os.path.join(os.path.dirname(__file__), "../../data/processed/analytics/yearly_trends.csv"))
    
    # 6. Time Series Analysis
    logging.info("Processing time series data...")
    monthly, yearly, rolling = time_series.build_time_series_analysis(df_financials.merge(clean_df[['listing_id', 'collected_at']], on='listing_id'))
    rolling.to_csv(os.path.join(os.path.dirname(__file__), "../../data/processed/analytics/time_series_rolling.csv"))
    
    # 7. MongoDB Aggregation (Optional fallback)
    try:
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        mongo_stats = mongo_pipeline.get_mongo_genre_stats(mongo_uri, "real_estate_db", "loopnet_listings")
        mongo_stats.to_csv(os.path.join(os.path.dirname(__file__), "../../data/processed/analytics/mongo_genre_stats.csv"))
        logging.info("MongoDB aggregation completed.")
    except Exception as e:
        logging.error(f"MongoDB aggregation failed: {e}")

    # 8. Insight Reporter (Quantified Questions)
    insight_reporter.run_all_questions(df_financials)
    
    print("✅ Advanced Analytics pipeline completed. Reports saved to data/processed/analytics/")

    # =================================================================
    # PHASE 9: LAB 11 - EMBEDDINGS AND VECTOR SEARCH
    # =================================================================
    logging.info("Starting Phase 9: Embeddings and Vector Search...")
    print("🧠 Running Phase 9: Embeddings and Vector Search...")

    from src.embeddings.embedder import Embedder
    from src.embeddings.chroma_store import ChromaStore

    # 1. Initialize Embedder and ChromaStore
    embedder = Embedder()
    store = ChromaStore(path=os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/embeddings/chroma_db")))

    # 2. Prepare and Add properties to ChromaDB (if empty or re-population requested)
    if store.count() == 0:
        logging.info("Populating ChromaDB with property embeddings...")
        documents = []
        metadatas = []
        ids = []
        
        for idx, row in clean_df.iterrows():
            doc = embedder.combine_property_fields(row)
            meta = {
                "title": str(row.get('title', 'Unknown')),
                "type": str(row.get('type', 'Commercial')),
                "listing_id": str(row.get('listing_id', idx))
            }
            documents.append(doc)
            metadatas.append(meta)
            ids.append(str(idx))
        
        # Generate embeddings explicitly to avoid ChromaDB downloading its own model
        print(f"🔄 Encoding {len(documents)} documents...")
        embeddings = embedder.generate_embeddings(documents)
        
        # Pass pre-computed embeddings
        store.add_properties(documents, metadatas, ids, embeddings=embeddings.tolist())
        print(f"✅ ChromaDB populated with {store.count()} property records.")
    else:
        print(f"📦 ChromaDB already contains {store.count()} records. Skipping re-population.")

    logging.info("Pipeline finished successfully")
    print("🏁 Pipeline finished successfully!")
    
    # Final step: Generate the summary report for the user
    generate_combined_report()

if __name__ == "__main__":
    run_pipeline()
