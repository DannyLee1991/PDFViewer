from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit
from pdfminer.layout import LTTextBoxHorizontal
from main.res import values as v
from main.tools.GoogleTranslate import get_translate
import os


class PdfPageWidget(QWidget):

    def __init__(self, parent, page):
        super().__init__(parent=parent)
        self.page = page
        self.setMinimumSize(700, 2024)
        self.initUI()

    def initUI(self):
        # self.all_text = ""
        vbox = QVBoxLayout()
        for x in self.page:
            if isinstance(x, LTTextBoxHorizontal):
                text = " ".join(x.get_text().split(os.linesep)).strip()
                ed_text = QTextEdit()
                ed_text.setText(text)
                ed_text.adjustSize()

                vbox.addWidget(ed_text)

                # ----添加翻译按钮----
                if len(text) > 5:
                    self.add_translate_bt(ed_text, text, vbox)

        self.setLayout(vbox)
        print("initUI")

    def add_translate_bt(self, ed_text, text, vbox):
        bt_translate = QPushButton(v.bt_translate)
        vbox.addWidget(bt_translate)
        bt_translate.tag = text
        bt_translate.bind = ed_text
        bt_translate.is_translate = False

        def do_translate():
            sender = self.sender()
            text = sender.tag
            if sender.is_translate:
                sender.bind.setText(text)
                sender.setText(v.bt_translate)
            else:
                translate_result = get_translate(text)
                trans_text = "".join(
                    list(filter(lambda item: item != None, [item[0] for item in translate_result])))
                sender.bind.setText(trans_text)
                sender.setText(v.bt_original)
            self.sender().is_translate = not self.sender().is_translate

        bt_translate.clicked.connect(do_translate)

    # def paintEvent(self, event):
    #     qp = QPainter()
    #     qp.begin(self)
    #     self.drawText(event, qp)
    #     qp.end()
    #     print('paintEvent')
    #
    # def drawText(self, event, qp):
    #
    #     qp.setPen(QColor(168, 34, 3))
    #     qp.setFont(QFont('Decorative', 10))
    #     qp.drawText(event.rect(), Qt.AlignCenter, self.all_text)
    #
    #     print('drawText')
    #     self.adjustSize()
    #     print("adjust height:" + str(self.height()))
