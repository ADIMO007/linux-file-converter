from src.converter.base_converter import BaseConverter

class ImageConverter(BaseConverter):
    def convert(self, input_file: str, output_format: str,
                output_dir: str = None, preset: dict = None) -> bool:
        """Convert image file"""
        output_path = self.get_output_path(input_file, output_format, output_dir)

        command = ['ffmpeg', '-i', input_file]

        if preset:
            if 'quality' in preset:
                command.extend(['-q:v', str(preset['quality'])])
            if 'compression' in preset:
                command.extend(['-compression_level', str(preset['compression'])])

        command.extend(['-y', output_path])

        return self.run_ffmpeg(command)
