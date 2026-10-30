# Linux File Conversion Utility

A lightweight, native Linux file conversion utility built with Python and PyQt5. It leverages existing system binaries (`ffmpeg`, `libreoffice`, `poppler-utils`) and lightweight Python packages to handle documents, media, images (including RAW camera files), comic archives (`.cbz`), and eBooks (`.epub`) entirely offline.

## Features
- **Documents & Spreadsheets:** PDF, DOCX, XLSX, ODT, HTML, TXT, RTF
- **Images & Camera RAW:** PNG, JPG, WEBP, TIFF, BMP, SVG, CR2, NEF, ARW, DNG, etc.
- **Comics & eBooks:** `.cbz` extraction/compilation, `.epub` conversion
- **Media:** MP3, WAV, FLAC, MP4, MKV, AVI

## Prerequisites & System Dependencies
Make sure you have the required system utilities installed on your Linux distribution:
```bash
sudo apt update && sudo apt install ffmpeg libreoffice poppler-utils pandoc -y
