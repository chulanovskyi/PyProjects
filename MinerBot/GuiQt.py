import sys
from MainSearch import *
from PyQt4 import QtGui, QtCore


class SearchThread(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

    def run(self):
        all_codes = scan_all()
        result = enter_all(all_codes)
        
        self.emit(QtCore.SIGNAL('codes'), 'New entries: {_result}'.format(_result=result))


class CustomOut(QtCore.QObject):
    text_wr = QtCore.pyqtSignal(str)

    def write(self, text):
        self.text_wr.emit(str(text))

        
class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        sys.stdout = CustomOut(text_wr=self.text_browser_out)

        self.app_ico = QtGui.QIcon('tray.ico')
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.auto_enter)
        self.timer.start(300000)
        
        self.setWindowTitle('GM')
        self.setWindowIcon(self.app_ico)
        self.resize(350,300)

        self.thread = SearchThread()

        self.vbox = QtGui.QVBoxLayout()
        self.setLayout(self.vbox)

        self.banner = QtGui.QLabel('<center>gameminer.net free giveaways</center>')
        self.vbox.addWidget(self.banner)

        self.to_tray = QtGui.QPushButton('Minimize to &tray',self)
        self.connect(self.to_tray,
                     QtCore.SIGNAL('clicked()'),
                     self.hide)
        self.vbox.addWidget(self.to_tray)
        
        self.text_browser = QtGui.QTextBrowser()
        self.char_format = QtGui.QTextCharFormat()
        self.text_browser.setOpenExternalLinks(True)
        self.text_browser.setReadOnly(True)
        self.vbox.addWidget(self.text_browser)

        self.result = QtGui.QLabel('...')
        self.connect(self.thread,
                     QtCore.SIGNAL('codes'),
                     self.on_change,
                     QtCore.Qt.QueuedConnection)
        self.vbox.addWidget(self.result)
        
        self.close = QtGui.QPushButton('&Close', self)
        self.connect(self.close,
                     QtCore.SIGNAL('clicked()'),
                     QtGui.qApp,
                     QtCore.SLOT('quit()'))
        self.vbox.addWidget(self.close)

        self.vbox.addStretch()

        self.sys_tray = QtGui.QSystemTrayIcon()
        self.sys_tray.setIcon(self.app_ico)
        self.sys_tray.setVisible(True)
        self.sys_tray.setToolTip(self.result.text())
        self.connect(self.sys_tray,
                     QtCore.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"),
                     self.sys_tray_activated)

        self.tray_menu = QtGui.QMenu(self)
        self.tray_show_action = self.tray_menu.addAction('Show', self.showNormal)
        self.tray_close_action = self.tray_menu.addAction('Close', QtGui.qApp.quit)
        self.sys_tray.setContextMenu(self.tray_menu)

        self.about = QtGui.QLabel('<center>---By SkyRocker---</center>')
        self.vbox.addWidget(self.about)

    def sys_tray_activated(self, reason):
        if reason == self.sys_tray.DoubleClick:
            self.setFocus(True)
            self.raise_()
            self.activateWindow()
            self.showNormal()
        
    def text_browser_out(self, text):
        state_code_name = text.split(None, 2)
        cursor = self.text_browser.textCursor()
        cursor_format = cursor.charFormat()
        cursor.movePosition(QtGui.QTextCursor.End)
        if 'Conditions\DLC: ' in text:
            cursor_format.setForeground(QtCore.Qt.red)
            cursor_format.setFontUnderline(True)
            cursor_format.setAnchorHref("http://gameminer.net/giveaway/"+state_code_name[1])
            cursor.setCharFormat(cursor_format)
            cursor.insertText(state_code_name[0] + ' ' + state_code_name[2])
        elif 'Entered: ' in text:
            cursor_format.setForeground(QtCore.Qt.blue)
            cursor_format.setFontUnderline(True)
            cursor_format.setAnchorHref("http://gameminer.net/giveaway/"+state_code_name[1])
            cursor.setCharFormat(cursor_format)
            cursor.insertText(state_code_name[0] + ' ' + state_code_name[2])
        else:
            cursor_format.setForeground(QtCore.Qt.black)
            cursor_format.UnderlineStyle(0)
            cursor_format.setFontUnderline(False)
            cursor_format.setAnchorHref(None)
            cursor.setCharFormat(cursor_format)
            cursor.insertText(text)

    def start_search(self):
        self.text_browser.clear()
        self.thread.start()

    def on_change(self, text):
        self.result.setText(text)

    def auto_enter(self):
        self.start_search()

    def minimize(self):
        self.hide()


if __name__ == '__main__':        
    main_app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    main_window.start_search()
    sys.exit(main_app.exec_())
