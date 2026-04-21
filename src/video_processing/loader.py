# --- LAB 7 AUDIO/VIDEO EXTENSION ---
import os
from moviepy import VideoFileClip
from utils.logger import logging

def load_video_and_extract_audio(video_path, audio_output_path):
    """
    Loads video, prints properties, extracts audio, and saves it as MP3.
    """
    try:
        logging.info(f"Loading video from {video_path}")
        clip = VideoFileClip(video_path)
        
        properties = {
            "duration": clip.duration,
            "fps": clip.fps,
            "resolution": clip.size,
            "has_audio": clip.audio is not None
        }
        
        print(f"\n--- Video Properties: {os.path.basename(video_path)} ---")
        for key, value in properties.items():
            print(f"{key.capitalize()}: {value}")
            
        if clip.audio:
            clip.audio.write_audiofile(audio_output_path, logger=None)
            logging.info(f"Audio extracted and saved to {audio_output_path}")
        
        clip.close()
        return properties
    except Exception as e:
        logging.error(f"Error loading video or extracting audio: {e}")
        return None
