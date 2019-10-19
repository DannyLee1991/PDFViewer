import sys
from PyQt5.QtWidgets import QFileDialog, QVBoxLayout
from main.view.windows.BsseQWidget import BaseQWidget
from main.view.widgets.PdfScrollWidget import PdfScrollWidget
from main.tools.PDFUtils import PDFUtils
from main.res import values as v
from main.tools.FileTypeUtils import is_pdf


class MainWindow(BaseQWidget):
    crt_pdf_pages = []

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 750, 1024)
        self.center()

        self.setWindowTitle(v.title)

        vbox = QVBoxLayout()
        vbox.addWidget(self.create_btn("open", clicked_callback=self.show_load_pdf_dialog))

        self.scroll_widget = PdfScrollWidget()
        vbox.addWidget(self.scroll_widget)

        self.setLayout(vbox)
        self.show()

    def closeEvent(self, event):
        self.quit_application()

    def show_load_pdf_dialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/')
        path = fname[0]
        if path:
            if is_pdf(path):
                self.crt_pdf_pages = PDFUtils().pdf2pages(path=path)
                self.on_pdf_loaded()
            else:
                self.show_msg_box(msg=v.msg_choose_pdf_file)

    def on_pdf_loaded(self):
        self.scroll_widget.load(self.crt_pdf_pages)
