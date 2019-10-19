import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QFileDialog, QPushButton, QMessageBox
from PyQt5.QtCore import QCoreApplication
from main.tools.PDFUtils import PDFUtils


class BaseQWidget(QWidget):
    def center(self):
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def quit_application(self):
        QCoreApplication.instance().quit()

    def show_msg_box(self, title='', msg="", t='a'):
        if t == 'i':
            reply = QMessageBox.information(
                self,
                title,
                msg,
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes)
        elif t == 'q':
            reply = QMessageBox.question(
                self,
                title,
                msg,
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes)
        elif t == 'w':
            reply = QMessageBox.warning(
                self,
                title,
                msg,
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes)
        elif t == 'c':
            reply = QMessageBox.critical(
                self,
                title,
                msg,
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes)
        else:
            reply = QMessageBox.about(
                self,
                title,
                msg)
        return reply

    def create_btn(self, name, clicked_callback=None, tip=""):
        # 创建一个PushButton并为他设置一个tooltip
        btn = QPushButton(name, self)
        if tip:
            btn.setToolTip(tip)
        # btn.sizeHint()显示默认尺寸
        btn.resize(btn.sizeHint())

        if clicked_callback:
            btn.clicked.connect(clicked_callback)
        return btn

    def on_pdf_load(self):
        pass
