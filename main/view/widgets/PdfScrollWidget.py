from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from main.view.widgets.PdfPageWidget import PdfPageWidget
import sip


class PdfScrollWidget(QScrollArea):
    vbox = QVBoxLayout()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.scroll = QWidget()
        self.setWidget(self.scroll)
        self.scroll.setLayout(self.vbox)

    def load(self, pages):
        # 清空布局
        for i in range(self.vbox.count()):
            if self.vbox.itemAt(i):
                w = self.vbox.itemAt(i).widget()
                self.vbox.removeWidget(w)
                sip.delete(w)

        total_height = 0
        for page in pages:
            ppw = PdfPageWidget(self, page)
            self.vbox.addWidget(ppw)
            h = ppw.height()
            print("page height : " + str(h))
            total_height += h
        self.scroll.setMinimumSize(self.width(), total_height)
