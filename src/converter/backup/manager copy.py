import json
from pathlib import Path
from typing import List, Dict
from src.converter.audio_converter import AudioConverter
from src.converter.video_converter import VideoConverter
from src.converter.image_converter import ImageConverter

class ConversionManager:
    def __init__(self):
        self.config_dir = Path.home() / '.config' / 'file-converter-linux'
        self.config_file = self.config_dir / 'presets.json'
        self.converters = {
            'audio': AudioConverter(),
            'video': VideoConverter(),
            'image': ImageConverter(),
        }
        self.load_presets()

    def load_presets(self):
        """Load conversion presets from config file"""
        presets_path = Path(__file__).parent.parent / 'config' / 'presets.json'
        if presets_path.exists():
            with open(presets_path, 'r') as f:
                self.presets = json.load(f)
        else:
            self.presets = self._default_presets()

    def _default_presets(self) -> Dict:
        """Return default presets"""
        return {
            'audio': {
                'mp3': {'codec': 'libmp3lame', 'bitrate': '192k', 'sample_rate': '44100'},
                'flac': {'codec': 'flac', 'bitrate': None, 'sample_rate': '44100'},
                'wav': {'codec': 'pcm_s16le', 'bitrate': None, 'sample_rate': '44100'},
                'ogg': {'codec': 'libvorbis', 'bitrate': '192k', 'sample_rate': '44100'},
                'aac': {'codec': 'aac', 'bitrate': '192k', 'sample_rate': '44100'},
            },
            'video': {
                'mp4': {'codec': 'libx264', 'preset': 'medium', 'crf': 23},
                'webm': {'codec': 'libvpx-vp9', 'preset': 'medium', 'crf': 30},
                'mkv': {'codec': 'libx264', 'preset': 'medium', 'crf': 23},
                'avi': {'codec': 'mpeg4', 'preset': 'medium', 'q:v': 5},
                'ogv': {'codec': 'libtheora', 'q:v': 7},
            },
            'image': {
                'jpg': {'quality': 85},
                'png': {'compression': 9},
                'webp': {'quality': 80},
                'avif': {'quality': 75},
                'ico': {'size': 256},
            }
        }

    def get_supported_formats(self, file_type: str) -> List[str]:
        """Get list of supported output formats for a file type"""
        return list(self.presets.get(file_type, {}).keys())

    def convert(self, input_file: str, output_format: str,
                file_type: str, output_dir: str = None) -> bool:
        """Convert file to specified format"""
        try:
            converter = self.converters.get(file_type)
            if not converter:
                return False

            preset = self.presets.get(file_type, {}).get(output_format, {})
            return converter.convert(input_file, output_format, output_dir, preset)
        except Exception as e:
            print(f"Conversion error: {e}")
            return False

    def get_file_type(self, filename: str) -> str:
        """Determine file type from extension"""
        ext = Path(filename).suffix.lower()[1:]
        for ftype, formats in self.presets.items():
            # Check in input formats list (simplified)
            if ftype == 'audio' and ext in ['mp3', 'wav', 'flac', 'aac', 'ogg', 'm4a', 'wma']:
                return 'audio'
            elif ftype == 'video' and ext in ['mp4', 'avi', 'mkv', 'webm', 'mov', 'flv']:
                return 'video'
            elif ftype == 'image' and ext in ['jpg', 'png', 'gif', 'bmp', 'ico', 'webp', 'tiff']:
                return 'image'
        return None
