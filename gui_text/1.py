# _*_coding:utf-8_*_
# author:leo
# date:
# email:alplf123@163.com

from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QWidget, QVBoxLayout, QFrame,QApplication, QWidget, QScrollArea, QLabel
from PyQt5.Qt import QSize
import sys

class Example(QMainWindow):

    def __init__(self):
        super(Example, self).__init__()

        self._initUI()
    def _initUI(self):
        #控件随窗口改变而改变
        # 可以通过继承 QMainWindow 来实现
        self.resize(700, 700)
        #建立顶层控件
        self.centeralwidget = QWidget()
        self.vbox = QVBoxLayout(self.centeralwidget)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_bar = self.scroll_area.verticalScrollBar()
        self.vbox.addWidget(self.scroll_area)

        self.scroll_contents = QWidget()
        self.scroll_contents.setGeometry(0, 0, 100, 600)
        self.scroll_contents.setMinimumSize(380, 1000)

        self.label_1 = QLabel(self.scroll_area)
        self.label_1.move(50, 100)
        self.label_1.setText("HelloRyan")

        self.label_2 = QLabel(self.scroll_area)
        self.label_2.move(50, 200)
        self.label_2.setText("你好")

        self.label_3 = QLabel(self.scroll_area)
        self.label_3.move(50, 300)
        self.label_3.setText("-----------")

        self.label_4 = QLabel(self.scroll_area)
        self.label_4.move(50, 400)
        self.label_4.setText("542543255235432543252")

        self.label_5 = QLabel(self.scroll_area)
        self.label_5.move(50, 500)
        self.label_5.setText("5432543262542")

        self.label_6 = QLabel(self.scroll_area)
        self.label_6.move(50, 2000)
        self.label_6.setText("4325432532")
        #通过设置中心控件，将子控件填充布局
        #如果有多个控件最好在加一层widget这样最好布局，控制
        self.setCentralWidget(self.centeralwidget)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())