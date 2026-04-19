# --- LAB 7 AUDIO/VIDEO EXTENSION ---
import os
from pydub import AudioSegment
from utils.logger import logging

def trim_audio(audio, start_ms, end_ms, output_path):
    """Trims audio to a specific segment and saves it."""
    try:
        trimmed = audio[start_ms:end_ms]
        trimmed.export(output_path, format=os.path.splitext(output_path)[1].replace('.', ''))
        logging.info(f"Trimmed audio saved to {output_path}")
        return trimmed
    except Exception as e:
        logging.error(f"Error trimming audio: {e}")
        return None

def concatenate_audio(clips, output_path):
    """Concatenates multiple audio clips and saves them."""
    try:
        if not clips:
            return None
        combined = clips[0]
        for clip in clips[1:]:
            combined += clip
        combined.export(output_path, format=os.path.splitext(output_path)[1].replace('.', ''))
        logging.info(f"Concatenated audio saved to {output_path}")
        return combined
    except Exception as e:
        logging.error(f"Error concatenating audio: {e}")
        return None

def adjust_volume(audio, gain_db):
    """Adjusts volume by gain_db (positive or negative)."""
    try:
        return audio + gain_db
    except Exception as e:
        logging.error(f"Error adjusting volume: {e}")
        return audio

def apply_fades(audio, fade_in_ms=0, fade_out_ms=0):
    """Applies fade-in and fade-out effects."""
    try:
        if fade_in_ms > 0:
            audio = audio.fade_in(fade_in_ms)
        if fade_out_ms > 0:
            audio = audio.fade_out(fade_out_ms)
        return audio
    except Exception as e:
        logging.error(f"Error applying fades: {e}")
        return audio

def convert_audio(audio, output_path):
    """Converts audio to another format."""
    try:
        format = os.path.splitext(output_path)[1].replace('.', '')
        audio.export(output_path, format=format)
        logging.info(f"Converted audio saved to {output_path} (format: {format})")
    except Exception as e:
        logging.error(f"Error converting audio: {e}")
