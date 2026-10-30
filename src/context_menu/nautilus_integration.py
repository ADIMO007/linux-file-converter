import os
from pathlib import Path

def setup_nautilus_extension():
    """Setup Nautilus context menu integration"""
    nautilus_dir = Path.home() / '.local' / 'share' / 'nautilus' / 'scripts'
    nautilus_dir.mkdir(parents=True, exist_ok=True)

    script_path = nautilus_dir / 'convert-file'

    script_content = '''#!/bin/bash
# File Converter Script for Nautilus

FILE="$NAUTILUS_SCRIPT_SELECTED_FILE_PATHS"

if [ -z "$FILE" ]; then
    zenity --error --text="Please select a file"
    exit 1
fi

# Extract filename
FILENAME=$(basename "$FILE")

# Launch converter with file
file-converter-linux --input "$FILE" &

exit 0
'''

    with open(script_path, 'w') as f:
        f.write(script_content)

    os.chmod(script_path, 0o755)
    print(f"Nautilus script installed at {script_path}")

def create_dolphin_service_menu():
    """Create KDE Dolphin service menu"""
    service_dir = Path.home() / '.local' / 'share' / 'kservices5' / 'ServiceMenus'
    service_dir.mkdir(parents=True, exist_ok=True)

    desktop_file = service_dir / 'convert-file.desktop'

    content = '''[Desktop Entry]
Type=Service
ServiceTypes=KonqPopupMenu/Plugin
MimeType=audio/*;video/*;image/*
Actions=ConvertFile

[Desktop Action ConvertFile]
Name=Convert File
Icon=media-optical
Exec=file-converter-linux --input %f
'''

    with open(desktop_file, 'w') as f:
        f.write(content)

    print(f"Dolphin service menu installed at {desktop_file}")
