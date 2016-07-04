import sys
from PyQt5 import QtGui
from PyQt5 import QtCore

class SystemTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtGui.QMenu(parent)
        exitAction = menu.addAction("Exit")
        self.setContextMenu(menu)

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        but = QtGui.QPushButton('butt',self)
        but.setGeometry(10,10,50,20)
        
        self.setGeometry(300,200,300, 200)
        self.setWindowTitle('Main')
        self.connect(but, QtCore.SIGNAL('clicked()'), QtGui.qApp, QtCore.SLOT('quit()'))
        self.statusBar().showMessage('Ready')

        self.show()

def main():
    app = QtGui.QApplication(sys.argv)

    screen = QtGui.QDesktopWidget().screenGeometry()
    
    #widget.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
    
    #window.connect(but, QtCore.SIGNAL('clicked()'), QtGui.qApp, QtCore.SLOT('quit()'))

    w = QtGui.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon("icon.png"), w)
    trayIcon.setToolTip('Progress')
    trayIcon.show()

    mainwindow = MainWindow()

    sys.exit(app.exec_())    


if __name__ == '__main__':
    main()
