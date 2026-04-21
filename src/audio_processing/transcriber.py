# --- LAB 7 AUDIO/VIDEO EXTENSION ---
import os
import json
from faster_whisper import WhisperModel
from pydub import AudioSegment
from utils.logger import logging

def transcribe_audio(file_path, model_size="base", output_base_path=None):
    """
    Transcribes a short audio file using faster-whisper with word-level timestamps.
    Saves to JSON, TXT, and SRT if output_base_path is provided.
    """
    try:
        logging.info(f"Transcribing {file_path} with model {model_size}")
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
        
        # Enable word_timestamps
        segments, info = model.transcribe(file_path, beam_size=5, word_timestamps=True)
        
        results = []
        full_text = ""
        srt_content = ""
        
        for i, segment in enumerate(segments):
            # Capture segments with timestamps and confidence scores
            results.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text,
                "avg_logprob": segment.avg_logprob, # Probability/confidence indicator
                "words": [{"start": w.start, "end": w.end, "word": w.word, "prob": w.probability} for w in (segment.words or [])]
            })
            full_text += segment.text + " "
            
            # Simple SRT format
            start_time = format_timestamp(segment.start)
            end_time = format_timestamp(segment.end)
            srt_content += f"{i+1}\n{start_time} --> {end_time}\n{segment.text.strip()}\n\n"
            
        if output_base_path:
            # Save JSON
            with open(f"{output_base_path}.json", "w", encoding="utf-8") as f:
                json.dump({"metadata": {"language": info.language, "model": model_size, "probability": info.language_probability}, "segments": results}, f, indent=4)
            # Save TXT
            with open(f"{output_base_path}.txt", "w", encoding="utf-8") as f:
                f.write(full_text.strip())
            # Save SRT
            with open(f"{output_base_path}.srt", "w", encoding="utf-8") as f:
                f.write(srt_content)
                
        return {"language": info.language, "text": full_text.strip(), "segments": results}
    except Exception as e:
        logging.error(f"Transcription error: {e}")
        return None

def chunked_transcribe(file_path, model_size="base", chunk_length_ms=300000, output_dir=None):
    """
    Transcribes a long audio file by splitting into chunks (default 5 mins) and combining results.
    Supports caching each chunk separately and progress tracking.
    """
    try:
        logging.info(f"Starting chunked transcription for {file_path}")
        audio = AudioSegment.from_file(file_path)
        chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
        
        num_chunks = len(chunks)
        all_text = ""
        all_segments = []
        
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        for i, chunk in enumerate(chunks):
            print(f"🔄 Processing chunk {i+1} of {num_chunks} for {os.path.basename(file_path)}...")
            chunk_name = f"{base_name}_chunk_{i}"
            chunk_json_path = os.path.join(output_dir, f"{chunk_name}.json") if output_dir else None
            
            # Cache check
            if chunk_json_path and os.path.exists(chunk_json_path):
                logging.info(f"Loading cached transcript for chunk {i}")
                with open(chunk_json_path, "r", encoding="utf-8") as f:
                    result = json.load(f)
            else:
                temp_chunk_path = f"temp_{chunk_name}.wav"
                chunk.export(temp_chunk_path, format="wav")
                
                result = transcribe_audio(temp_chunk_path, model_size=model_size, 
                                        output_base_path=os.path.join(output_dir, chunk_name) if output_dir else None)
                
                if os.path.exists(temp_chunk_path):
                    os.remove(temp_chunk_path)
            
            if result:
                all_text += result["text"] + " "
                # Adjust timestamps for segments and words
                offset = (i * chunk_length_ms) / 1000.0
                for seg in result["segments"]:
                    new_seg = seg.copy()
                    new_seg["start"] += offset
                    new_seg["end"] += offset
                    if "words" in new_seg:
                        for w in new_seg["words"]:
                            w["start"] += offset
                            w["end"] += offset
                    all_segments.append(new_seg)
            
        combined_result = {"text": all_text.strip(), "segments": all_segments}
        
        # Save combined result
        if output_dir:
            combined_json_path = os.path.join(output_dir, f"{base_name}_combined.json")
            with open(combined_json_path, "w", encoding="utf-8") as f:
                json.dump(combined_result, f, indent=4)
            logging.info(f"Combined transcription saved to {combined_json_path}")
            
        return combined_result
    except Exception as e:
        logging.error(f"Chunked transcription error: {e}")
        return None

def format_timestamp(seconds):
    """Formats seconds into SRT timestamp (HH:MM:SS,ms)."""
    td = seconds
    hours = int(td // 3600)
    minutes = int((td % 3600) // 60)
    secs = int(td % 60)
    milliseconds = int((td % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"
