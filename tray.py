import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import time
import weather


class Worker(QObject):
    finished = pyqtSignal()
    temp = pyqtSignal(int)

    def run(self):
        while True:
            self.temp.emit(weather.get_current_temp())
            self.finished.emit()
            time.sleep(30)


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip("Now")
        menu = QtWidgets.QMenu(parent)
        menu.setTitle('qwerty')
        settingsAction = menu.addAction('Settings')
        exitAction = menu.addAction('Exit')
        #updateWeather = menu.addAction('Update')
        exitAction.triggered.connect(self.exit)
        settingsAction.triggered.connect(self.settings)
        self.setContextMenu(menu)
        self.update()

    def exit(self):
        sys.exit()

    def settings(self):
        print('settings')
        self.next = Settings()


    def update(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.temp.connect(self.setIcon)
        self.thread.start()

    def setIcon(self, temp):
        icon = QtGui.QIcon(f"resources\\{temp}.bmp")
        super(SystemTrayIcon, self).setIcon(icon)
        self.setToolTip(f'Now is {temp}')

class Settings(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("qdialog")
        self.show()

app = QtWidgets.QApplication(sys.argv)
w = QtWidgets.QWidget()
tray_icon = SystemTrayIcon(QtGui.QIcon("resources\\thermometer.png"), w)
tray_icon.show()
sys.exit(app.exec())
