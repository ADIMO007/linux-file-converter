#!/usr/bin/env python3
import sys
import json
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from src.gui.main_window import MainWindow
from src.context_menu.nautilus_integration import setup_nautilus_extension
from src.converter.manager import ConversionManager

class FileConverterApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.config_dir = Path.home() / '.config' / 'file-converter-linux'
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Initialize converter manager
        self.converter_manager = ConversionManager()

        # Setup nautilus integration
        setup_nautilus_extension()

        # Create main window
        self.window = MainWindow(self.converter_manager)

    def run(self):
        self.window.show()
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    app = FileConverterApp()
    app.run()
