# --- LAB 7 AUDIO/VIDEO EXTENSION ---
import os
from pydub import AudioSegment
from utils.logger import logging

def load_audio(file_path):
    """
    Loads audio in various formats (WAV, MP3, FLAC, OGG) and prints properties.
    """
    try:
        logging.info(f"Loading audio from {file_path}")
        # Determine format from extension
        extension = os.path.splitext(file_path)[1].lower().replace('.', '')
        
        # Load audio segment
        audio = AudioSegment.from_file(file_path, format=extension)
        
        # Extract properties
        properties = {
            "format": extension,
            "duration_sec": len(audio) / 1000.0,
            "channels": audio.channels,
            "frame_rate": audio.frame_rate,
            "sample_width": audio.sample_width,
            "bit_depth": audio.sample_width * 8,
            "file_size_bytes": os.path.getsize(file_path)
        }
        
        print(f"\n--- Audio Properties: {os.path.basename(file_path)} ---")
        for key, value in properties.items():
            print(f"{key.replace('_', ' ').capitalize()}: {value}")
        
        return audio
    except Exception as e:
        logging.error(f"Error loading audio {file_path}: {e}")
        return None
