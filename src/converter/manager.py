import os
from .audio_converter import AudioConverter
from .video_converter import VideoConverter
from .image_converter import ImageConverter
from .pdf_converter import PDFConverter


class ConversionManager:
    def __init__(self):
        self.converters = {
            'audio': AudioConverter(),
            'video': VideoConverter(),
            'image': ImageConverter(),
            'pdf': PDFConverter()
        }

        # Map extensions directly to converter categories
        self.EXTENSION_MAP = {
            'pdf': 'pdf', 'docx': 'pdf', 'doc': 'pdf',
            'cbz': 'pdf',
            'xlsx': 'pdf', 'xls': 'pdf',
            'pptx': 'pdf', 'ppt': 'pdf',
            'odt': 'pdf', 'ods': 'pdf', 'odp': 'pdf', 'html': 'pdf',

            'png': 'image', 'jpg': 'image', 'jpeg': 'image', 'webp': 'image',

            'mp3': 'audio', 'wav': 'audio', 'aac': 'audio', 'flac': 'audio', 'ogg': 'audio',

            'mp4': 'video', 'mkv': 'video', 'avi': 'video', 'mov': 'video'
        }

        # Supported target output formats mapped per input extension
        self.SUPPORTED_FORMATS = {
            # PDF conversions
            'pdf': ['png', 'jpg', 'jpeg', 'webp', 'bmp', 'tiff', 'svg', 'docx', 'odt', 'html', 'txt', 'rtf', 'epub', 'cbz'],

            # CBZ comic files can be converted to PDF, EPUB, or PNG/JPG image pages
            'cbz': ['pdf', 'epub', 'png', 'jpg'],

            # Office Document conversions
            'docx': ['pdf', 'odt', 'txt', 'rtf', 'html'],
            'doc': ['pdf', 'odt', 'txt', 'rtf'],
            'rtf': ['pdf', 'docx', 'odt', 'txt'],
            'txt': ['pdf', 'docx', 'odt'],

            # Spreadsheet conversions
            'xlsx': ['pdf', 'ods', 'csv', 'html'],
            'xls': ['pdf', 'ods', 'csv'],
            'csv': ['pdf', 'xlsx', 'ods'],

            # Presentation conversions
            'pptx': ['pdf', 'odp'],
            'ppt': ['pdf', 'odp'],

            # Image conversions
            'jpg': ['pdf', 'png', 'webp', 'bmp', 'tiff'],
            'jpeg': ['pdf', 'png', 'webp', 'bmp', 'tiff'],
            'png': ['pdf', 'jpg', 'jpeg', 'webp', 'bmp', 'tiff', 'ico'],
            'webp': ['pdf', 'png', 'jpg', 'jpeg', 'bmp'],
            'bmp': ['pdf', 'png', 'jpg', 'webp'],
            'tiff': ['pdf', 'png', 'jpg'],

            # Audio & Video conversions
            'mp3': ['wav', 'aac', 'flac', 'ogg', 'm4a'],
            'wav': ['mp3', 'aac', 'flac', 'ogg'],
            'flac': ['mp3', 'wav', 'aac'],
            'mp4': ['mkv', 'avi', 'mov', 'mp3', 'webm'],
            'mkv': ['mp4', 'avi', 'mov', 'mp3'],
            'avi': ['mp4', 'mkv', 'mov']
        }

    def get_file_type(self, file_path: str):
        """Extracts extension and returns category string."""
        ext = os.path.splitext(file_path)[1].lower().strip('.')
        return self.EXTENSION_MAP.get(ext, None)

    def get_supported_formats(self, file_path_or_ext: str) -> list:
        """Extracts extension cleanly and returns supported formats list."""
        ext = os.path.splitext(file_path_or_ext)[1].lower().strip('.')
        if not ext:
            ext = file_path_or_ext.lower().strip('.')
        return self.SUPPORTED_FORMATS.get(ext, [])

    def convert(self, input_file: str, output_format: str, file_type: str) -> bool:
        """Executes conversion logic."""
        try:
            output_dir = os.path.dirname(input_file)
            ext = os.path.splitext(input_file)[1].lower().strip('.')
            base_name = os.path.splitext(os.path.basename(input_file))[0]

            if file_type == 'pdf':
                pdf_conv = self.converters['pdf']

                if ext == 'cbz' and output_format == 'pdf':
                    pdf_conv.cbz_to_pdf(input_file, output_dir)
                    return True
                elif ext == 'pdf' and output_format in ['png', 'jpg', 'jpeg', 'webp']:
                    pdf_conv.pdf_to_images(input_file, output_dir, fmt=output_format)
                elif ext == 'pdf':
                    pdf_conv.pdf_to_office(input_file, output_dir, target_ext=output_format)
                elif output_format == 'pdf':
                    if ext in ['doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx']:
                        pdf_conv.office_to_pdf(input_file, output_dir)
                    elif ext in ['png', 'jpg', 'jpeg', 'webp']:
                        out_pdf = os.path.join(output_dir, f"{base_name}.pdf")
                        pdf_conv.images_to_pdf([input_file], out_pdf)

            elif file_type == 'image':
                out_path = os.path.join(output_dir, f"{base_name}.{output_format}")
                self.converters['image'].convert_image(input_file, out_path)

            elif file_type == 'audio':
                out_path = os.path.join(output_dir, f"{base_name}.{output_format}")
                self.converters['audio'].convert_audio(input_file, out_path)

            elif file_type == 'video':
                out_path = os.path.join(output_dir, f"{base_name}.{output_format}")
                self.converters['video'].convert_video(input_file, out_path)

            return True
        except Exception as e:
            print(f"[Conversion Error]: {e}")
            return False
