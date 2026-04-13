import os
from datetime import datetime
from tqdm import tqdm
from pathlib import Path

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import logging
from image_processing.processor import (
    inspect_image, resize_proportional, generate_thumbnail, 
    convert_to_webp, enhance_image
)
from image_processing.exif_utils import get_exif_data, get_gps_coordinates
from storage.mongo import save_image_metadata
from utils.upload_utils import upload_batch

def process_single(image_path, property_data=None):
    """Run a single property image through the entire pipeline."""
    try:
        if property_data is None:
            property_data = {}
            
        logging.info(f"Processing image: {image_path}")
        
        # 1. Inspect
        info = inspect_image(image_path)
        if not info:
            return None
            
        # 2. Extract EXIF
        exif = get_exif_data(image_path)
        gps = get_gps_coordinates(exif)
        
        # 3. Process
        resized_path = resize_proportional(image_path)
        thumb_path = generate_thumbnail(image_path)
        webp_path = convert_to_webp(image_path)
        enhanced_path = enhance_image(image_path)
        
        # 4. Prepare Metadata
        metadata = {
            "property_id": property_data.get("propertyId") or property_data.get("id"),
            "address": property_data.get("address"),
            "source": "LoopNet",
            "type": "exterior", # Placeholder
            "filename": os.path.basename(image_path),
            "original_path": str(image_path),
            "resized_path": str(resized_path),
            "thumbnail_path": str(thumb_path),
            "webp_path": str(webp_path),
            "enhanced_path": str(enhanced_path),
            "format": info["format"],
            "mode": info["mode"],
            "width": info["size"][0],
            "height": info["size"][1],
            "aspect_ratio": info["size"][0] / info["size"][1],
            "file_size_kb": info["file_size_kb"],
            "exif": exif,
            "gps": gps,
            "processed_at": datetime.now().isoformat()
        }
        
        return metadata, [webp_path, thumb_path] # Return metadata and files to upload
        
    except Exception as e:
        logging.error(f"Error in process_single for {image_path}: {e}")
        return None

def batch_process_images(images_dir, loopnet_data=None):
    """Iterates over a folder of downloaded property images and processes them."""
    images_dir = Path(images_dir)
    image_files = list(images_dir.glob("*.jpg")) + list(images_dir.glob("*.jpeg")) + list(images_dir.glob("*.png")) + list(images_dir.glob("*.webp"))
    
    all_metadata = []
    all_files_to_upload = []
    
    # Map loopnet data by property_id for easier lookup if filename contains id
    data_map = {}
    if loopnet_data:
        for item in loopnet_data:
            pid = str(item.get("propertyId") or item.get("id"))
            data_map[pid] = item

    logging.info(f"Starting batch process for {len(image_files)} images.")
    
    for img_path in tqdm(image_files, desc="Batch Processing"):
        # Try to find matching property data
        filename = img_path.name
        property_id = None
        if "property_" in filename:
            property_id = filename.split("_")[1].split(".")[0]
        
        prop_data = data_map.get(property_id, {"id": property_id})
        
        result = process_single(img_path, prop_data)
        if result:
            metadata, upload_files = result
            all_metadata.append(metadata)
            all_files_to_upload.extend(upload_files)
            
    # Save to MongoDB
    if all_metadata:
        save_image_metadata(all_metadata)
        
    # Upload to Google Drive
    if all_files_to_upload:
        logging.info(f"Uploading {len(all_files_to_upload)} files to Google Drive.")
        upload_batch(all_files_to_upload)
        
    logging.info("Batch processing complete.")
    return all_metadata

if __name__ == "__main__":
    # Example usage:
    # batch_process_images("data/raw/property_images")
    pass
