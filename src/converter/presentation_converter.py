import subprocess
from pathlib import Path
from src.converter.base_converter import BaseConverter


class PresentationConverter(BaseConverter):
    """Converter for Presentation files (PPT, PPTX to Video)."""

    def check_dependencies(self):
        try:
            subprocess.run(["soffice", "--version"], capture_output=True, check=True)
            subprocess.run(["pdftoppm", "-v"], capture_output=True, check=True)
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            raise RuntimeError(
                "LibreOffice (soffice), Poppler-utils (pdftoppm), and FFmpeg must be installed."
            )

    def convert(
        self, input_file: str, output_dir: str = None, duration_per_slide: int = 4
    ) -> str:
        self.check_dependencies()
        input_path = Path(input_file)
        out_dir = Path(output_dir) if output_dir else input_path.parent
        temp_dir = out_dir / "temp_slides"
        temp_dir.mkdir(parents=True, exist_ok=True)

        try:
            # Step 1: Export PPT/PPTX slides as PDF using LibreOffice headless
            print(f"[PresentationConverter] Converting {input_path.name} to PDF...")
            subprocess.run(
                [
                    "soffice",
                    "--headless",
                    "--convert-to",
                    "pdf",
                    str(input_path),
                    "--outdir",
                    str(temp_dir),
                ],
                check=True,
            )

            # Locate the generated PDF file
            pdf_file = temp_dir / f"{input_path.stem}.pdf"
            if not pdf_file.exists():
                # Fallback if LibreOffice used spaces or modified the name
                pdf_files = list(temp_dir.glob("*.pdf"))
                if not pdf_files:
                    raise RuntimeError(
                        "LibreOffice failed to generate a PDF from the presentation."
                    )
                pdf_file = pdf_files[0]

            # Step 2: Convert PDF pages to PNG images using pdftoppm
            # Using -img -r 150 and prefix 'slide' -> produces slide-1.png, slide-2.png, etc.
            print("[PresentationConverter] Rendering slides to images...")
            subprocess.run(
                ["pdftoppm", "-png", "-r", "150", str(pdf_file), str(temp_dir / "slide")],
                check=True,
            )

            # Output MP4 path
            output_mp4 = out_dir / f"{input_path.stem}.mp4"

            # Step 3: Combine slide images into an MP4 video using FFmpeg
            # Note: pdftoppm outputs 1-indexed single digits (slide-1.png, slide-2.png...) unless padded.
            # We use glob pattern or standard single-digit pattern %d.png for robustness.
            print("[PresentationConverter] Stitching slides into video via FFmpeg...")
            ffmpeg_cmd =[
                "ffmpeg",
                "-y",
                "-framerate",
                f"1/{duration_per_slide}",
                "-i",
                str(temp_dir / "slide-%d.png"),
                "-c:v",
                "libx264",
                "-vf",
                "scale=trunc(iw/2)*2:trunc(ih/2)*2",  # <--- Forces even dimensions for libx264
                "-r",
                "30",
                "-pix_fmt",
                "yuv420p",
                str(output_mp4),
            ]
            subprocess.run(ffmpeg_cmd, check=True)

            print(f"[PresentationConverter] Success! Video saved to {output_mp4}")
            return str(output_mp4)

        finally:
            # Cleanup temporary files (PDF and PNGs)
            if temp_dir.exists():
                for file in temp_dir.glob("*"):
                    file.unlink()
                temp_dir.rmdir()
