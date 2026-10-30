import subprocess
from pathlib import Path
from typing import Dict

class BaseConverter:
    """Base class for all converters"""

    def __init__(self):
        self.check_dependencies()

    def check_dependencies(self):
        """Check if required tools are installed"""
        try:
            subprocess.run(['ffmpeg', '-version'],
                         capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError("FFmpeg is not installed. Please install it first.")

    def convert(self, input_file: str, output_format: str,
                output_dir: str = None, preset: Dict = None) -> bool:
        """Convert file - implemented by subclasses"""
        raise NotImplementedError

    def get_output_path(self, input_file: str, output_format: str,
                       output_dir: str = None) -> str:
        """Generate output file path"""
        input_path = Path(input_file)
        output_filename = input_path.stem + f'.{output_format}'

        if output_dir:
            return str(Path(output_dir) / output_filename)
        return str(input_path.parent / output_filename)

    def run_ffmpeg(self, command: list) -> bool:
        """Execute FFmpeg command"""
        try:
            result = subprocess.run(command, capture_output=True,
                                  text=True, timeout=3600)
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            print("Conversion timeout")
            return False
        except Exception as e:
            print(f"FFmpeg error: {e}")
            return False
