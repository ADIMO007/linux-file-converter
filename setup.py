from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="file-converter-linux",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A cross-platform file converter for Linux with context menu support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/file-converter-linux",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications :: Qt",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyQt5>=5.15.0",
        "PyQtWebEngine>=5.15.0",
        "python-xlib>=0.33",
    ],
    entry_points={
        "console_scripts": [
            "file-converter-linux=src.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["config/*.json", "icons/*.png"],
    },
)
