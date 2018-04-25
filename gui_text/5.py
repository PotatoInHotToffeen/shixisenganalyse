# _*_coding:utf-8_*_
import sys
import analyse
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QScrollArea, QLabel,QDesktopWidget,QMainWindow,QVBoxLayout)
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import QEvent

class FirstWindow(QWidget):

    def __init__(self):
        super(FirstWindow, self).__init__()
        self.windowUI()

    def windowUI(self):
        self.setWindowTitle("Login")
        self.textfield()
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def textfield(self):
        QToolTip.setFont(QFont('SansSerif', 12))
        user = QLabel("User:")
        userEdit = QLineEdit()
        userEdit.setToolTip("请输入你的帐号")

        passWord = QLabel("PassWord:")
        passWordEdit = QLineEdit()
        passWordEdit.setToolTip("请输入你的密码")

        grid = QGridLayout()
        grid.setSpacing(0)

        grid.addWidget(user, 0, 0)
        grid.addWidget(userEdit, 1, 0)
        grid.addWidget(passWord, 2, 0)
        grid.addWidget(passWordEdit, 3, 0)
        empty = QLabel()
        grid.addWidget(empty, 4, 0)

        btn_logon = QPushButton("Log on")
        btn_quit = QPushButton("Quit")
        grid.addWidget(btn_logon, 5, 0, 1, 2)
        grid.addWidget(btn_quit, 6, 0, 1, 2)

        btn_logon.clicked.connect(self.onclick)
        btn_quit.clicked.connect(quit)

        self.setLayout(grid)

    def onclick(self):
        analyse.test()
        newWindow = MainWindow()
        newWindow.show()
        newWindow.exec_()

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

if __name__ == "__main__":
    App = QApplication(sys.argv)
    ex = FirstWindow()
    ex.show()
    sys.exit(App.exec_())