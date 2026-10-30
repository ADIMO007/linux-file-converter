import os
import glob
import zipfile
import shutil
import subprocess
from .base_converter import BaseConverter


class PDFConverter(BaseConverter):
    def check_dependencies(self):
        try:
            subprocess.run(["pdftoppm", "-v"], capture_output=True, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            print("Warning: pdftoppm not found.")

    def cbz_to_pdf(self, input_cbz: str, output_dir: str):
        """Extracts images from a .cbz archive and compiles them into a single PDF."""
        base_name = os.path.splitext(os.path.basename(input_cbz))[0]
        temp_dir = os.path.join(output_dir, f"_temp_{base_name}")
        os.makedirs(temp_dir, exist_ok=True)

        try:
            print(f"[CBZ Debug] Extracting {input_cbz}...")
            with zipfile.ZipFile(input_cbz, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            valid_exts = ('.png', '.jpg', '.jpeg', '.webp', '.bmp')
            image_paths = []
            for root, _, files in os.walk(temp_dir):
                for f in sorted(files):
                    if f.lower().endswith(valid_exts):
                        image_paths.append(os.path.join(root, f))

            print(f"[CBZ Debug] Found {len(image_paths)} images.")
            if not image_paths:
                raise ValueError("No valid images found inside the CBZ file.")

            out_pdf = os.path.join(output_dir, f"{base_name}.pdf")
            print(f"[CBZ Debug] Generating PDF at {out_pdf}...")
            self.images_to_pdf(image_paths, out_pdf)
            print("[CBZ Debug] Conversion complete!")

        except Exception as e:
            print(f"[CBZ Error] Failed: {e}")
            raise e
        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

    def pdf_to_cbz(self, input_pdf: str, output_dir: str, dpi: int = 300):
        """Renders PDF pages to PNG images and bundles them into a .cbz archive."""
        base_name = os.path.splitext(os.path.basename(input_pdf))[0]
        temp_dir = os.path.join(output_dir, f"_temp_{base_name}")
        os.makedirs(temp_dir, exist_ok=True)

        try:
            output_prefix = os.path.join(temp_dir, f"{base_name}_page")
            cmd = ["pdftoppm", "-png", "-r", str(dpi), input_pdf, output_prefix]
            subprocess.run(cmd, check=True)

            cbz_path = os.path.join(output_dir, f"{base_name}.cbz")
            with zipfile.ZipFile(cbz_path, 'w', zipfile.ZIP_DEFLATED) as zip_out:
                for png_file in sorted(glob.glob(os.path.join(temp_dir, "*.png"))):
                    arcname = os.path.basename(png_file)
                    zip_out.write(png_file, arcname=arcname)

        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

    def convert_epub(self, input_file: str, output_dir: str, target_ext: str):
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(output_dir, f"{base_name}.{target_ext}")

        if subprocess.run(["which", "ebook-convert"], capture_output=True).returncode == 0:
            cmd = ["ebook-convert", input_file, output_file]
            subprocess.run(cmd, check=True)
        else:
            cmd = ["libreoffice", "--headless", "--convert-to", target_ext, input_file, "--outdir", output_dir]
            subprocess.run(cmd, check=True)

    def pdf_to_images(self, input_pdf: str, output_dir: str, fmt: str = "png", dpi: int = 300):
        base_name = os.path.splitext(os.path.basename(input_pdf))[0]
        output_prefix = os.path.join(output_dir, f"{base_name}_page")
        fmt = fmt.lower().strip('.')

        if fmt in ['jpg', 'jpeg']:
            cmd = ["pdftoppm", "-jpeg", "-r", str(dpi), input_pdf, output_prefix]
            subprocess.run(cmd, check=True)
        elif fmt == 'png':
            cmd = ["pdftoppm", "-png", "-r", str(dpi), input_pdf, output_prefix]
            subprocess.run(cmd, check=True)
        elif fmt in ['tiff', 'tif']:
            cmd = ["pdftoppm", "-tiff", "-r", str(dpi), input_pdf, output_prefix]
            subprocess.run(cmd, check=True)
        elif fmt == 'svg':
            output_svg_pattern = os.path.join(output_dir, f"{base_name}_page-%d.svg")
            cmd = ["pdf2svg", input_pdf, output_svg_pattern]
            subprocess.run(cmd, check=True)
        elif fmt in ['webp', 'bmp', 'gif']:
            cmd_png = ["pdftoppm", "-png", "-r", str(dpi), input_pdf, output_prefix]
            subprocess.run(cmd_png, check=True)

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
        if subprocess.run(["which", "magick"], capture_output=True).returncode == 0:
            cmd = ["magick"] + image_paths + [output_pdf]
        elif subprocess.run(["which", "convert"], capture_output=True).returncode == 0:
            cmd = ["convert"] + image_paths + [output_pdf]
        else:
            cmd = ["ffmpeg", "-y", "-i", image_paths[0], output_pdf]
        subprocess.run(cmd, check=True)

    def office_to_pdf(self, input_file: str, output_dir: str):
        cmd = ["libreoffice", "--headless", "--convert-to", "pdf", input_file, "--outdir", output_dir]
        subprocess.run(cmd, check=True)

    def pdf_to_office(self, input_pdf: str, output_dir: str, target_ext: str = "docx"):
        cmd = ["libreoffice", "--headless", "--infilter=writer_pdf_import", "--convert-to", target_ext, input_pdf, "--outdir", output_dir]
        subprocess.run(cmd, check=True)
