import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from pathlib import Path

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import logging

def get_exif_data(image_path):
    """Extracts all EXIF tags from a JPG photo."""
    exif_data = {}
    try:
        with Image.open(image_path) as img:
            info = img._getexif()
            if info:
                for tag, value in info.items():
                    decoded = TAGS.get(tag, tag)
                    if decoded == "GPSInfo":
                        gps_data = {}
                        for t in value:
                            sub_decoded = GPSTAGS.get(t, t)
                            gps_data[sub_decoded] = value[t]
                        exif_data[decoded] = gps_data
                    else:
                        exif_data[decoded] = value
        return exif_data
    except Exception as e:
        logging.error(f"Error extracting EXIF from {image_path}: {e}")
        return {}

def get_gps_coordinates(exif_data):
    """Extracts GPS coordinates from EXIF data."""
    if "GPSInfo" not in exif_data:
        return None

    def _convert_to_degrees(value):
        d = float(value[0])
        m = float(value[1])
        s = float(value[2])
        return d + (m / 60.0) + (s / 3600.0)

    gps_info = exif_data["GPSInfo"]
    gps_latitude = gps_info.get("GPSLatitude")
    gps_latitude_ref = gps_info.get("GPSLatitudeRef")
    gps_longitude = gps_info.get("GPSLongitude")
    gps_longitude_ref = gps_info.get("GPSLongitudeRef")

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        lat = _convert_to_degrees(gps_latitude)
        if gps_latitude_ref != "N":
            lat = 0 - lat

        lon = _convert_to_degrees(gps_longitude)
        if gps_longitude_ref != "E":
            lon = 0 - lon

        return lat, lon
    return None

def get_exif_summary(image_path):
    """Returns a summary of important EXIF data."""
    exif = get_exif_data(image_path)
    if not exif:
        return "No EXIF data found."
    
    summary = {
        "Make": exif.get("Make"),
        "Model": exif.get("Model"),
        "DateTime": exif.get("DateTime"),
        "Software": exif.get("Software"),
        "GPS": get_gps_coordinates(exif)
    }
    return summary

def save_clean_image(image_path):
    """Saves a clean copy of the image without any EXIF metadata."""
    try:
        with Image.open(image_path) as img:
            data = list(img.getdata())
            image_without_exif = Image.new(img.mode, img.size)
            image_without_exif.putdata(data)
            
            project_root = Path(__file__).resolve().parent.parent.parent
            clean_dir = project_root / "data" / "processed" / "clean"
            clean_dir.mkdir(parents=True, exist_ok=True)
            
            output_path = clean_dir / f"clean_{os.path.basename(image_path)}"
            image_without_exif.save(output_path)
            return str(output_path)
    except Exception as e:
        logging.error(f"Error cleaning EXIF from {image_path}: {e}")
        return None
