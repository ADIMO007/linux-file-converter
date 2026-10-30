import subprocess
import shutil
from .base_converter import BaseConverter


class ImageConverter(BaseConverter):
    def check_dependencies(self):
        # Check if either 'magick' or 'convert' (ImageMagick) or 'ffmpeg' is installed
        if not (shutil.which("magick") or shutil.which("convert") or shutil.which("ffmpeg")):
            print("Warning: Neither ImageMagick nor FFmpeg found for image conversions.")

    def convert_image(self, input_path: str, output_path: str):
        """
        Converts image formats (PNG, JPG, WEBP, etc.) independently using
        system CLI tools (ImageMagick or FFmpeg fallback).
        """
        # Option A: Try ImageMagick ('magick' or 'convert')
        cmd = None
        if shutil.which("magick"):
            cmd = ["magick", input_path, output_path]
        elif shutil.which("convert"):
            cmd = ["convert", input_path, output_path]
        # Option B: Fallback to FFmpeg (FFmpeg natively converts images too!)
        elif shutil.which("ffmpeg"):
            cmd = ["ffmpeg", "-y", "-i", input_path, output_path]

        if cmd:
            subprocess.run(cmd, check=True)
        else:
            raise RuntimeError("No image conversion tool found. Install ImageMagick or FFmpeg.")
