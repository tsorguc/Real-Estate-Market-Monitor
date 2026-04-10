import os
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
from pathlib import Path

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import logging

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RESIZED_DIR = PROJECT_ROOT / "data" / "processed" / "resized"
THUMBNAILS_DIR = PROJECT_ROOT / "data" / "processed" / "thumbnails"
CROPPED_DIR = PROJECT_ROOT / "data" / "processed" / "cropped"
WEBP_DIR = PROJECT_ROOT / "data" / "processed" / "webp"

for d in [RESIZED_DIR, THUMBNAILS_DIR, CROPPED_DIR, WEBP_DIR]:
    d.mkdir(parents=True, exist_ok=True)

def inspect_image(image_path):
    """Prints size, mode, format, and file size of an image."""
    try:
        with Image.open(image_path) as img:
            file_size = os.path.getsize(image_path) / 1024 # KB
            print(f"--- Image Info: {os.path.basename(image_path)} ---")
            print(f"Size: {img.size}")
            print(f"Mode: {img.mode}")
            print(f"Format: {img.format}")
            print(f"File Size: {file_size:.2f} KB")
            return {
                "size": img.size,
                "mode": img.mode,
                "format": img.format,
                "file_size_kb": file_size
            }
    except Exception as e:
        logging.error(f"Error inspecting image {image_path}: {e}")
        return None

def resize_proportional(image_path, base_width=1024):
    """Resizes high-res property photos to standard web sizes proportionally."""
    try:
        with Image.open(image_path) as img:
            w_percent = (base_width / float(img.size[0]))
            h_size = int((float(img.size[1]) * float(w_percent)))
            img = img.resize((base_width, h_size), Image.Resampling.LANCZOS)
            
            output_path = RESIZED_DIR / f"resized_{os.path.basename(image_path)}"
            img.save(output_path)
            logging.info(f"Resized image saved to {output_path}")
            return str(output_path)
    except Exception as e:
        logging.error(f"Error resizing image {image_path}: {e}")
        return None

def resize_image(image_path, size=(1024, 768)):
    """Resizes image to a specific size."""
    try:
        with Image.open(image_path) as img:
            img = img.resize(size, Image.Resampling.LANCZOS)
            output_path = RESIZED_DIR / f"fixed_{os.path.basename(image_path)}"
            img.save(output_path)
            return str(output_path)
    except Exception as e:
        logging.error(f"Error resizing image {image_path}: {e}")
        return None

def generate_thumbnail(image_path, size=(256, 256)):
    """Generates a thumbnail using Pillow's thumbnail()."""
    try:
        with Image.open(image_path) as img:
            img.thumbnail(size)
            output_path = THUMBNAILS_DIR / f"thumb_{os.path.basename(image_path)}"
            img.save(output_path)
            return str(output_path)
    except Exception as e:
        logging.error(f"Error generating thumbnail for {image_path}: {e}")
        return None

def generate_fixed_thumbnail(image_path, size=(256, 256)):
    """Generates a fixed-size thumbnail using ImageOps.fit()."""
    try:
        with Image.open(image_path) as img:
            img = ImageOps.fit(img, size, Image.Resampling.LANCZOS)
            output_path = THUMBNAILS_DIR / f"fixed_thumb_{os.path.basename(image_path)}"
            img.save(output_path)
            return str(output_path)
    except Exception as e:
        logging.error(f"Error generating fixed thumbnail for {image_path}: {e}")
        return None

def crop_image(image_path, crop_box=(100, 100, 400, 400)):
    """Crops an image using a 4-tuple (left, upper, right, lower)."""
    try:
        with Image.open(image_path) as img:
            img = img.crop(crop_box)
            output_path = CROPPED_DIR / f"cropped_{os.path.basename(image_path)}"
            img.save(output_path)
            return str(output_path)
    except Exception as e:
        logging.error(f"Error cropping image {image_path}: {e}")
        return None

def convert_to_webp(image_path):
    """Converts image to WebP format."""
    try:
        with Image.open(image_path) as img:
            filename = Path(image_path).stem + ".webp"
            output_path = WEBP_DIR / filename
            img.save(output_path, "WEBP")
            return str(output_path)
    except Exception as e:
        logging.error(f"Error converting image {image_path} to WebP: {e}")
        return None

def convert_to_grayscale(image_path):
    """Converts image to grayscale."""
    try:
        with Image.open(image_path) as img:
            img = img.convert("L")
            output_path = WEBP_DIR / f"gray_{os.path.basename(image_path)}"
            img.save(output_path)
            return str(output_path)
    except Exception as e:
        logging.error(f"Error converting image {image_path} to grayscale: {e}")
        return None

def save_optimised_jpeg(image_path, quality=85):
    """Saves image as an optimized JPEG."""
    try:
        with Image.open(image_path) as img:
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            output_path = WEBP_DIR / f"opt_{Path(image_path).stem}.jpg"
            img.save(output_path, "JPEG", optimize=True, quality=quality)
            return str(output_path)
    except Exception as e:
        logging.error(f"Error optimizing JPEG for {image_path}: {e}")
        return None

def apply_filters(image_path):
    """Applies BLUR and SHARPEN filters."""
    results = {}
    try:
        with Image.open(image_path) as img:
            blurred = img.filter(ImageFilter.BLUR)
            blur_path = WEBP_DIR / f"blur_{os.path.basename(image_path)}"
            blurred.save(blur_path)
            results['blur'] = str(blur_path)
            
            sharpened = img.filter(ImageFilter.SHARPEN)
            sharp_path = WEBP_DIR / f"sharp_{os.path.basename(image_path)}"
            sharpened.save(sharp_path)
            results['sharpen'] = str(sharp_path)
        return results
    except Exception as e:
        logging.error(f"Error applying filters to {image_path}: {e}")
        return None

def enhance_image(image_path, brightness=1.2, contrast=1.2, sharpness=1.2, color=1.2):
    """Enhances image brightness, contrast, sharpness, and color."""
    try:
        with Image.open(image_path) as img:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(brightness)
            
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast)
            
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(sharpness)
            
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(color)
            
            output_path = WEBP_DIR / f"enhanced_{os.path.basename(image_path)}"
            img.save(output_path)
            return str(output_path)
    except Exception as e:
        logging.error(f"Error enhancing image {image_path}: {e}")
        return None
