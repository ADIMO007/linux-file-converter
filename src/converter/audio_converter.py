from src.converter.base_converter import BaseConverter

class AudioConverter(BaseConverter):
    def convert(self, input_file: str, output_format: str,
                output_dir: str = None, preset: dict = None) -> bool:
        """Convert audio file"""
        output_path = self.get_output_path(input_file, output_format, output_dir)

        # Build FFmpeg command
        command = ['ffmpeg', '-i', input_file]

        if preset:
            if 'bitrate' in preset and preset['bitrate']:
                command.extend(['-b:a', preset['bitrate']])
            if 'codec' in preset:
                command.extend(['-c:a', preset['codec']])
            if 'sample_rate' in preset:
                command.extend(['-ar', str(preset['sample_rate'])])

        command.extend(['-y', output_path])  # -y: overwrite output file

        return self.run_ffmpeg(command)
