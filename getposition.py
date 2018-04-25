# _*_coding:utf-8_*_
from PyQt5.QtCore import*
from PyQt5.QtWidgets import QWidget, QApplication, QGroupBox, QPushButton, QLabel, QHBoxLayout,  QVBoxLayout, QGridLayout, QFormLayout, QLineEdit, QTextEdit

import resultshow
import analyse
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class login(QWidget):
    def __init__(self):
        super(login,self).__init__()
        self.initUi()
        self.name =""
    def initUi(self):
        self.setWindowTitle("login")
        layout = QGridLayout()
        self.setGeometry(600, 600, 400, 400)


        nameLabel = QLabel("姓名")
        self.nameLineEdit = QLineEdit(" ")
        layout.addWidget(nameLabel,1,0)
        layout.addWidget(self.nameLineEdit,1,1)
        layout.setColumnStretch(1, 10)
        save_Btn = QPushButton('保存')
        cancle_Btn = QPushButton('取消')
        cancle_Btn.clicked.connect(QCoreApplication.quit)
        save_Btn.clicked.connect(self.addNum)
        layout.addWidget(save_Btn)
        layout.addWidget(cancle_Btn)
        self.setLayout(layout)

    def addNum(self):
        position = self.nameLineEdit.text()  # 获取文本框内容
        analyse.test()
        # f=open('position.txt','w')
        # f.write(position)
        # f.close()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = login()
    mainwindow.show()
    sys.exit(app.exec_())
    resultshow.show()

