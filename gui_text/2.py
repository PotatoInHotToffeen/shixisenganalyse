# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QScrollArea, QLabel,QDesktopWidget,QMainWindow,QVBoxLayout)
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import QEvent


class FirstWindow(QWidget):

    # close_signal = pyqtSignal()
    def __init__(self, parent=None):
        # super这个用法是调用父类的构造函数
        # parent=None表示默认没有父Widget，如果指定父亲Widget，则调用之
        super(FirstWindow, self).__init__(parent)
        self.resize(100, 100)
        self.btn = QToolButton(self)
        self.btn.setText("click")

    # def closeEvent(self, event):
    #     self.close_signal.emit()
    #     self.close()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self._initUI()

    def _initUI(self):
        w = QWidget()
        self.setCentralWidget(w)

        topFiller = QWidget()
        topFiller.setStyleSheet("background-color:white;")
        topFiller.setMinimumSize (1200, 8000)


        for i in range(1,11):
            path='C:/Users/Braggart/PycharmProjects/nice/analysephoto/'+str(i)+'.png'
            png=QtGui.QPixmap(path)
            label1 = QLabel(topFiller)
            label1.setPixmap(png)
            label1.move(250, (i-1)*750)

            label2 = QLabel(topFiller)
            file=open('C:/Users/Braggart/PycharmProjects/nice/analysephoto/'+str(i)+'.txt')
            label2.setText(file.read())
            label2.move(300, (i)*750-100)
            label2.setFont(QFont("Microsoft YaHei",11, 75))


        scroll = QScrollArea()
        scroll.setWidget(topFiller)
        scroll.setAutoFillBackground(True)
        scroll.setWidgetResizable(True)

        vbox = QVBoxLayout()
        vbox.addWidget(scroll)
        w.setLayout(vbox)


        self.statusBar().showMessage(self.tr(u"最终解释权归杨欣越所有"))
        self.setWindowTitle(self.tr("Menus"))
        self.resize(700,320)


    def handle_click(self):
        if not self.isVisible():
            self.show()

    def handle_close(self):
        self.close()

# class SecondWindow(QWidget):
#     def __init__(self, parent=None):
#         super(SecondWindow, self).__init__(parent)
#         self.resize(200, 200)
#         self.setStyleSheet("background: black")
#
#     def handle_click(self):
#         if not self.isVisible():
#             self.show()
#
#     def handle_close(self):
#         self.close()


if __name__ == "__main__":
    App = QApplication(sys.argv)
    ex = FirstWindow()
    s = MainWindow()
    ex.btn.clicked.connect(s.handle_click)
    ex.btn.clicked.connect(ex.hide)
    # ex.close_signal.connect(ex.close)
    ex.show()
    sys.exit(App.exec_())