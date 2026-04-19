# Real-Estate-Market-Monitor
My Unstructured Data Repo

## Lab 7: Audio and Video Processing

This lab extends the pipeline with audio and video processing capabilities.

### Learning Objectives
- Load and inspect audio/video files
- Process audio (trim, concatenate, adjust volume, fades, convert)
- Extract audio from video
- Extract keyframes from video
- Transcribe audio using `faster-whisper` (short and long audio with chunking)
- Store transcripts in MongoDB

### Video Processing
Video properties extraction and audio track separation.
![Video Properties Placeholder](data/processed/frames/video_properties_sample.png)

### Audio Transcription
Transcription with word-level timestamps using `faster-whisper`.
![Transcription Sample](data/processed/transcripts/transcription_sample.png)

### Pipeline Integration
All activities are logged to `pipeline.log` and transcripts are stored in MongoDB.
