"""
video_scraper.py
Module for extracting short, playable video clips from live HLS streams (YouTube).
"""
import logging
import subprocess
import sys
from pathlib import Path

# Configuring logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def download_live_clip(
    video_url: str, 
    output_dir: Path, 
    clip_name: str = "revelstoke_sample", 
    duration_sec: int = 10
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = output_dir / f"{clip_name}.mp4"

    command = [
        sys.executable,
        "-m",
        "yt_dlp",
        "--no-part",
        "--downloader", "ffmpeg",
        "--downloader-args", f"ffmpeg:-t {duration_sec}",
        "--recode-video", "mp4",
        "-o", str(output_path),
        video_url
    ]

    logger.info(f"Starting live stream capture for {duration_sec} seconds...")

    result = subprocess.run(
        command,
        check=False, capture_output=True,
        text=True
    )

    if result.returncode != 0:
        logger.error(f"yt-dlp failed:\n{result.stderr}")
    else:
        logger.info("Capture completed successfully.")

    return output_path

if __name__ == "__main__":
    TARGET_URL = "https://www.youtube.com/watch?v=fIMbMz2P7Bs"
    RAW_DATA_DIR = Path("data/raw")

    logger.info("Initializing Video Scraper...")
    downloaded_file = download_live_clip(
        video_url=TARGET_URL,
        output_dir=RAW_DATA_DIR,
        duration_sec=10
    )

    if downloaded_file.exists():
        size_mb = downloaded_file.stat().st_size / (1024 * 1024)
        logger.info(f"SUCCESS: File saved at {downloaded_file}. Size: {size_mb:.2f} MB")
    else:
        logger.error("FAILED: Download failed. File does not exist.")