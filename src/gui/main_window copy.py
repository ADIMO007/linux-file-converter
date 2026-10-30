from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QFileDialog, QComboBox,
                             QProgressBar, QMessageBox, QListWidget, QListWidgetItem)
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from pathlib import Path

class ConversionWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool)

    def __init__(self, manager, input_file, output_format, file_type):
        super().__init__()
        self.manager = manager
        self.input_file = input_file
        self.output_format = output_format
        self.file_type = file_type

    def run(self):
        result = self.manager.convert(self.input_file, self.output_format, self.file_type)
        self.finished.emit(result)

class MainWindow(QMainWindow):
    def __init__(self, converter_manager):
        super().__init__()
        self.manager = converter_manager
        self.input_file = None
        self.file_type = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('File Converter Linux')
        self.setGeometry(100, 100, 600, 400)

        # Set icon
        icon_path = Path(__file__).parent.parent.parent / 'icons' / 'app_icon.png'
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # File selection
        file_layout = QHBoxLayout()
        self.file_label = QLabel('No file selected')
        file_btn = QPushButton('Select File')
        file_btn.clicked.connect(self.select_file)
        file_layout.addWidget(QLabel('Input:'))
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(file_btn)
        layout.addLayout(file_layout)

        # Format selection
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel('Output Format:'))
        self.format_combo = QComboBox()
        format_layout.addWidget(self.format_combo)
        layout.addLayout(format_layout)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        # Convert button
        convert_btn = QPushButton('Convert')
        convert_btn.clicked.connect(self.convert)
        layout.addWidget(convert_btn)

        # Recent files
        layout.addWidget(QLabel('Recent Files:'))
        self.recent_list = QListWidget()
        layout.addWidget(self.recent_list)

        central_widget.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select File')
        if file_path:
            self.input_file = file_path
            self.file_type = self.manager.get_file_type(file_path)

            if not self.file_type:
                QMessageBox.warning(self, 'Error', 'Unsupported file type')
                return

            self.file_label.setText(Path(file_path).name)
            self.update_format_combo()

    def update_format_combo(self):
        if self.file_type:
            formats = self.manager.get_supported_formats(self.file_type)
            self.format_combo.clear()
            self.format_combo.addItems(formats)

    def convert(self):
        if not self.input_file:
            QMessageBox.warning(self, 'Error', 'Please select a file')
            return

        output_format = self.format_combo.currentText()
        if not output_format:
            QMessageBox.warning(self, 'Error', 'Please select output format')
            return

        self.progress.setVisible(True)
        self.worker = ConversionWorker(self.manager, self.input_file,
                                       output_format, self.file_type)
        self.worker.finished.connect(self.on_conversion_finished)
        self.worker.start()

    def on_conversion_finished(self, success):
        self.progress.setVisible(False)
        if success:
            QMessageBox.information(self, 'Success', 'File converted successfully')
        else:
            QMessageBox.critical(self, 'Error', 'Conversion failed')
