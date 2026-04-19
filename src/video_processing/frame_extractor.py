import os
import json
from moviepy import VideoFileClip
from utils.logger import logging

def extract_keyframes(video_path, output_dir, interval_seconds=10):
    """
    Extracts keyframes from a video at regular intervals and saves them as PNG images.
    Also saves a JSON manifest of extracted frames.
    """
    try:
        logging.info(f"Extracting frames from {video_path} every {interval_seconds} seconds")
        clip = VideoFileClip(video_path)
        
        duration = clip.duration
        frames_extracted = []
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        
        for t in range(0, int(duration), interval_seconds):
            frame_filename = f"{base_name}_frame_{t}.png"
            frame_path = os.path.join(output_dir, frame_filename)
            clip.save_frame(frame_path, t=t)
            
            frames_extracted.append({
                "timestamp_sec": t,
                "file_path": frame_path,
                "filename": frame_filename
            })
            
        # Save JSON manifest
        manifest_path = os.path.join(output_dir, f"{base_name}_frames_manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump({"video_source": video_path, "frames": frames_extracted}, f, indent=4)
            
        logging.info(f"Extracted {len(frames_extracted)} frames to {output_dir}")
        clip.close()
        return len(frames_extracted)
    except Exception as e:
        logging.error(f"Error extracting frames: {e}")
        return 0
