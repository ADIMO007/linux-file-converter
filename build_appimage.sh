#!/bin/bash

# File Converter Linux - AppImage Builder
# This script builds a standalone AppImage for Linux

set -e

REPO_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
BUILD_DIR="$REPO_DIR/build"
APPIMAGE_DIR="$BUILD_DIR/FileConverter.AppDir"
PYTHON_VERSION="3.11"
APPIMAGE_TOOL_URL="https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== File Converter Linux - AppImage Builder ===${NC}"

# Step 1: Clean previous builds
echo -e "${YELLOW}Step 1: Cleaning previous builds...${NC}"
rm -rf "$BUILD_DIR"
mkdir -p "$APPIMAGE_DIR/usr/bin"
mkdir -p "$APPIMAGE_DIR/usr/lib"
mkdir -p "$APPIMAGE_DIR/usr/share/applications"
mkdir -p "$APPIMAGE_DIR/usr/share/icons"

# Step 2: Create Python virtual environment
echo -e "${YELLOW}Step 2: Creating Python environment...${NC}"
python3 -m venv "$APPIMAGE_DIR/usr"
source "$APPIMAGE_DIR/usr/bin/activate"

# Step 3: Install dependencies
echo -e "${YELLOW}Step 3: Installing dependencies...${NC}"
pip install --upgrade pip setuptools wheel
pip install -r "$REPO_DIR/requirements.txt"

# Step 4: Install the application
echo -e "${YELLOW}Step 4: Installing application...${NC}"
pip install -e "$REPO_DIR"

# Step 5: Copy application files
echo -e "${YELLOW}Step 5: Copying application files...${NC}"
cp -r "$REPO_DIR/src" "$APPIMAGE_DIR/usr/lib/file-converter-linux/"
cp -r "$REPO_DIR/icons" "$APPIMAGE_DIR/usr/share/icons/file-converter-linux/"

# Step 6: Create AppRun script
echo -e "${YELLOW}Step 6: Creating AppRun script...${NC}"
cat > "$APPIMAGE_DIR/AppRun" << 'EOF'
#!/bin/bash
SELF=$(readlink -f "$0")
HERE="${SELF%/*}"
export LD_LIBRARY_PATH="${HERE}/usr/lib:${HERE}/usr/lib/x86_64-linux-gnu:${LD_LIBRARY_PATH}"
export PATH="${HERE}/usr/bin:${PATH}"
export PYTHONPATH="${HERE}/usr/lib/python3.11/site-packages:${PYTHONPATH}"

exec "$HERE/usr/bin/python3" -m src.main "$@"
EOF
chmod +x "$APPIMAGE_DIR/AppRun"

# Step 7: Create desktop entry
echo -e "${YELLOW}Step 7: Creating desktop entry...${NC}"
cat > "$APPIMAGE_DIR/usr/share/applications/file-converter-linux.desktop" << 'EOF'
[Desktop Entry]
Type=Application
Name=File Converter Linux
Comment=Convert files between different formats
Exec=file-converter-linux
Icon=file-converter-linux
Categories=Utility;
Terminal=false
MimeType=audio/*;video/*;image/*;
EOF

# Step 8: Copy icon
echo -e "${YELLOW}Step 8: Copying icon...${NC}"
if [ -f "$REPO_DIR/icons/app_icon.png" ]; then
    mkdir -p "$APPIMAGE_DIR/usr/share/icons/hicolor/256x256/apps"
    cp "$REPO_DIR/icons/app_icon.png" "$APPIMAGE_DIR/usr/share/icons/hicolor/256x256/apps/file-converter-linux.png"
else
    echo -e "${RED}Warning: Icon file not found${NC}"
fi

# Step 9: Download AppImage tool
echo -e "${YELLOW}Step 9: Downloading AppImage tool...${NC}"
if [ ! -f "$BUILD_DIR/appimagetool" ]; then
    wget -q "$APPIMAGE_TOOL_URL" -O "$BUILD_DIR/appimagetool"
    chmod +x "$BUILD_DIR/appimagetool"
fi

# Step 10: Build AppImage
echo -e "${YELLOW}Step 10: Building AppImage...${NC}"
cd "$BUILD_DIR"
./appimagetool "$APPIMAGE_DIR" "FileConverter-x86_64.AppImage"

echo -e "${GREEN}=== AppImage build complete! ===${NC}"
echo -e "${GREEN}AppImage created at: $BUILD_DIR/FileConverter-x86_64.AppImage${NC}"
echo -e "${GREEN}To use it:${NC}"
echo -e "${YELLOW}1. chmod +x $BUILD_DIR/FileConverter-x86_64.AppImage${NC}"
echo -e "${YELLOW}2. ./$BUILD_DIR/FileConverter-x86_64.AppImage${NC}"
