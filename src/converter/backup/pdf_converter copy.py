import os
import glob
import subprocess
from .base_converter import BaseConverter


class PDFConverter(BaseConverter):
    def check_dependencies(self):
        try:
            subprocess.run(["pdftoppm", "-v"], capture_output=True, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            print("Warning: pdftoppm (poppler-utils) not found.")

        try:
            subprocess.run(["libreoffice", "--version"], capture_output=True, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            print("Warning: LibreOffice not found.")

    def pdf_to_images(self, input_pdf: str, output_dir: str, fmt: str = "png", dpi: int = 300):
        """Converts PDF pages into images (PNG, JPG, WEBP, TIFF, BMP, SVG)."""
        base_name = os.path.splitext(os.path.basename(input_pdf))[0]
        output_prefix = os.path.join(output_dir, f"{base_name}_page")
        fmt = fmt.lower().strip('.')

        # 1. Native Poppler outputs (PNG, JPEG, TIFF)
        if fmt in ['jpg', 'jpeg']:
            cmd = ["pdftoppm", "-jpeg", "-r", str(dpi), input_pdf, output_prefix]
            subprocess.run(cmd, check=True)
            return

        elif fmt == 'png':
            cmd = ["pdftoppm", "-png", "-r", str(dpi), input_pdf, output_prefix]
            subprocess.run(cmd, check=True)
            return

        elif fmt in ['tiff', 'tif']:
            cmd = ["pdftoppm", "-tiff", "-r", str(dpi), input_pdf, output_prefix]
            subprocess.run(cmd, check=True)
            return

        # 2. PDF to SVG (Vector graphics)
        elif fmt == 'svg':
            output_svg_pattern = os.path.join(output_dir, f"{base_name}_page-%d.svg")
            cmd = ["pdf2svg", input_pdf, output_svg_pattern]
            subprocess.run(cmd, check=True)
            return

        # 3. Formats requiring conversion pass (WEBP, BMP, GIF)
        elif fmt in ['webp', 'bmp', 'gif']:
            # Render to PNG first
            cmd_png = ["pdftoppm", "-png", "-r", str(dpi), input_pdf, output_prefix]
            subprocess.run(cmd_png, check=True)

            # Convert intermediate PNG files to the target format
            rendered_pngs = glob.glob(os.path.join(output_dir, f"{base_name}_page-*.png"))
            for png_file in rendered_pngs:
                target_file = os.path.splitext(png_file)[0] + f".{fmt}"

                if subprocess.run(["which", "magick"], capture_output=True).returncode == 0:
                    subprocess.run(["magick", png_file, target_file], check=True)
                elif subprocess.run(["which", "convert"], capture_output=True).returncode == 0:
                    subprocess.run(["convert", png_file, target_file], check=True)
                else:
                    subprocess.run(["ffmpeg", "-y", "-i", png_file, target_file], check=True)

                os.remove(png_file)

    def images_to_pdf(self, image_paths: list, output_pdf: str):
        """Combines single or multiple images into a PDF."""
        if subprocess.run(["which", "magick"], capture_output=True).returncode == 0:
            cmd = ["magick"] + image_paths + [output_pdf]
        elif subprocess.run(["which", "convert"], capture_output=True).returncode == 0:
            cmd = ["convert"] + image_paths + [output_pdf]
        else:
            cmd = ["ffmpeg", "-y", "-i", image_paths[0], output_pdf]

        subprocess.run(cmd, check=True)

    def office_to_pdf(self, input_file: str, output_dir: str):
        """Converts DOCX, XLSX, PPTX, RTF, TXT to PDF."""
        cmd = [
            "libreoffice", "--headless", "--convert-to", "pdf",
            input_file, "--outdir", output_dir
        ]
        subprocess.run(cmd, check=True)

    def pdf_to_office(self, input_pdf: str, output_dir: str, target_ext: str = "docx"):
        """Converts PDF to DOCX, ODT, HTML, TXT, RTF, EPUB."""
        cmd = [
            "libreoffice", "--headless", "--infilter=writer_pdf_import",
            "--convert-to", target_ext, input_pdf, "--outdir", output_dir
        ]
        subprocess.run(cmd, check=True)
