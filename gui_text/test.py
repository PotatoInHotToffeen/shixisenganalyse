from PyQt4 import QtGui,QtCore  
import sys  
class Web_Browser(QtGui.QDialog):  
    def __init__(self,parent=None):  
        QtGui.QWidget.__init__(self)  
        self.resize(550,400)  
        open=QtGui.QPushButton('OPEN')  
        self.connect(open,QtCore.SIGNAL('clicked()'),self.ok)  
        grid=QtGui.QGridLayout()  
        grid.addWidget(open,1,0,1,1)  
        self.setLayout(grid)  
        self.setWindowTitle('main windows')      
    def ok(self):  
        web=Web_Browser()  
        web.setModal(False)  
        web.setWindowTitle('sub window')  
        web.exec_()  
  
app=QtGui.QApplication(sys.argv)  
  
app.setFont(QtGui.QFont("Helvetica", 16))  
main=Web_Browser()  
main.show()  
  
sys.exit(app.exec_())  