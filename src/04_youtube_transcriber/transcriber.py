"""
YouTube Transcriber
===================
Extracts subtitles/transcripts from YouTube videos using video ID or URL.
(Wraps youtube_transcript_api CLI for stability)
"""

import argparse
import os
import re
import subprocess
import sys

def extract_video_id(url_or_id):
    """
    Extracts video ID from a typical YouTube URL or returns the ID if it looks like one.
    """
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
        r"^([0-9A-Za-z_-]{11})$"
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    return url_or_id

def get_transcript_cli(video_id, lang='ja'):
    """Fetch transcript using the CLI wrapper."""
    try:
        # Construct command: youtube_transcript_api [id] --languages [lang] --format text
        cmd = [
            "youtube_transcript_api",
            video_id,
            "--languages", lang, "en", # Try requested language, then English
            "--format", "text"
        ]
        
        # Run command without text=True to capture bytes
        process = subprocess.run(cmd, capture_output=True)
        
        if process.returncode != 0:
            # Try decoding stderr for error message
            try:
                err = process.stderr.decode('utf-8')
            except:
                err = process.stderr.decode('cp932', errors='ignore')
            raise Exception(err)
            
        # Try decoding stdout
        try:
            return process.stdout.decode('utf-8')
        except UnicodeDecodeError:
            return process.stdout.decode('cp932', errors='ignore')
        
    except Exception as e:
        print(f"❌ Error fetching transcript: {e}")
        return None

def save_to_file(text, video_id):
    filename = f"transcript_{video_id}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"✅ Saved to: {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube Transcriber")
    parser.add_argument("target", nargs="?", help="YouTube Video URL or ID")
    parser.add_argument("--lang", default="ja", help="Language code (default: ja)")
    
    args = parser.parse_args()
    
    target = args.target
    if not target:
        print("--- YouTube Transcriber ---")
        target = input("🔗 Enter YouTube URL or ID: ").strip()
        
    if not target:
        print("❌ Error: No target specified.")
        sys.exit(1)
    
    vid = extract_video_id(target)
    print(f"🎬 Target Video ID: {vid}")
    print(f"⏳ Fetching subtitles...")
    
    # Check if youtube_transcript_api is installed
    try:
        subprocess.run(["youtube_transcript_api", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("❌ Error: 'youtube_transcript_api' command not found. Please install dependencies.")
        sys.exit(1)

    text = get_transcript_cli(vid, args.lang)
    
    if text:
        save_to_file(text, vid)
        print("--- Preview ---")
        preview_lines = text.strip().split("\n")[:3]
        for line in preview_lines:
            print(line)
        print("...")
