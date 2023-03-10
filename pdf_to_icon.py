import os

from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem
from pdf2image import convert_from_path

from utils import get_pdf_thumbnail


class PdfToIcon(QThread):
    finished = pyqtSignal()

    def __init__(self, window, pdfs):
        super(PdfToIcon, self).__init__()
        self.window = window
        self.pdfs = pdfs

    def run(self):
        for file_path in self.pdfs:
            for page_num in range(len(convert_from_path(file_path))):
                item = QListWidgetItem()
                item.setIcon(QIcon(get_pdf_thumbnail(file_path, page_num=page_num + 1)))
                item.setText(os.path.basename(file_path) + f"\n page: {page_num + 1}")
                item.setData(Qt.UserRole, (file_path, page_num))
                self.window.addItem(item)
        self.finished.emit()
