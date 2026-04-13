import os
import requests
import json
from dotenv import load_dotenv
from pathlib import Path
from tqdm import tqdm

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import logging

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RAW_IMAGES_DIR = PROJECT_ROOT / "data" / "raw" / "property_images"
RAW_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

def download_image(url, filename):
    """Download an image from a URL and save it to the raw images directory."""
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        
        filepath = RAW_IMAGES_DIR / filename
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return str(filepath)
    except Exception as e:
        logging.error(f"Failed to download image {url}: {e}")
        return None

def fetch_and_download_images(data_list):
    """Extract image URLs from LoopNet data and download them."""
    downloaded_files = []
    logging.info(f"Starting image download for {len(data_list)} items.")
    
    for item in tqdm(data_list, desc="Downloading Images"):
        # LoopNet API items typically have an 'imageUrl' or 'images' list
        # This structure might vary depending on the actual API response
        image_url = item.get('imageUrl') or item.get('mainImage', {}).get('url')
        property_id = item.get('propertyId') or item.get('id')
        
        if image_url and property_id:
            extension = image_url.split('.')[-1].split('?')[0]
            if extension not in ['jpg', 'jpeg', 'png', 'webp']:
                extension = 'jpg' # Default extension
            
            filename = f"property_{property_id}.{extension}"
            filepath = download_image(image_url, filename)
            if filepath:
                item['local_image_path'] = filepath
                downloaded_files.append(filepath)
        
        # If there are multiple images
        additional_images = item.get('images', [])
        if isinstance(additional_images, list):
            for i, img in enumerate(additional_images[:3]): # Limit to first 3 additional images
                img_url = img if isinstance(img, str) else img.get('url')
                if img_url:
                    filename = f"property_{property_id}_extra_{i}.jpg"
                    download_image(img_url, filename)

    logging.info(f"Successfully downloaded {len(downloaded_files)} images.")
    return downloaded_files

if __name__ == "__main__":
    # Test with sample data if needed
    pass
