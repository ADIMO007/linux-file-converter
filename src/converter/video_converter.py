import os
import subprocess
from .base_converter import BaseConverter


class VideoConverter(BaseConverter):
    def check_dependencies(self):
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            print("Warning: ffmpeg not found.")

    def convert_video(self, input_path: str, output_path: str):
        """Converts video formats using ffmpeg with safe space handling and error logs."""
        cmd = ["ffmpeg", "-y", "-i", input_path, output_path]

        try:
            print(f"[Video Debug] Input: {input_path}")
            print(f"[Video Debug] Output: {output_path}")

            # Run ffmpeg and capture output for debugging
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print("[Video Debug] Conversion successful!")

        except subprocess.CalledProcessError as e:
            print(f"[Video Error] FFmpeg failed with exit code {e.returncode}")
            print(f"[Video Error Details]: {e.stderr}")
            raise e
