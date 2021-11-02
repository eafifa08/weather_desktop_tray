"""
weather app for desktop by Sergey Meshkov
"""
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QRunnable, QThreadPool, pyqtSlot
import time
import weather
import settings
import ctypes


class Main(QObject):

    temp = pyqtSignal(int)

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.city = settings.read_config('settings.ini', 'city')
        self.period = int(settings.read_config('settings.ini', 'period'))
        self.w = QtWidgets.QWidget()
        self.gui = SystemTrayIcon(QtGui.QIcon("resources\\thermometer.png"), self.w)
        self.createWorkerThread(self.city, self.period)
        self._connectSignals()
        self.gui.show()

    def createWorkerThread(self, city, period):
        # Setup the worker object and the worker_thread.
        self.worker = Worker(city, period)
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()
        #self.worker_thread.started.connect(self.worker.run)
        self.gui.startAction.triggered.connect(self.worker.run)

    def _connectSignals(self):
        #self.gui.stopAction.triggered.connect(self.forceWorkerQuit)
        self.gui.stopAction.triggered.connect(self.forceWorkerReset)
        self.temp.connect(self.gui.setIcon)
        self.parent().aboutToQuit.connect(self.forceWorkerQuit)

    def forceWorkerReset(self):
        if self.worker_thread.isRunning():
            print('Terminating thread.')
            self.worker_thread.terminate()
            print('Waiting for thread termination.')
            self.worker_thread.wait()
            self.signalStatus.emit('Reset')
            #self.temp.emit('Idle.')
            #print('building new working object.')
            self.createWorkerThread()

    def forceWorkerQuit(self):
        if self.worker_thread.isRunning():
            self.worker_thread.terminate()
            self.worker_thread.wait()


class Worker(QObject):
    #finished = pyqtSignal()
    temp = pyqtSignal(int)

    def __init__(self, city, period, parent=None):
        super(self.__class__, self).__init__(parent)
        self.city = city
        self.period = period

    @pyqtSlot()
    def run(self):
        while True:
            self.temp.emit(weather.get_current_temp(self.city))
            #self.finished.emit(1)
            #self.my_continue = False
            print('sleep')
            time.sleep(self.period)

    def change_settings(self, city, period):
        self.city = city
        self.period = period


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        user32 = ctypes.windll.user32
        self.screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        print(self.screensize)

        self.setToolTip("Now")
        self.menu = QtWidgets.QMenu(parent)
        self.menu.setTitle('qwerty')
        self.settingsAction = self.menu.addAction('Settings')
        self.changeSettingsAction = self.menu.addAction('Change settings')
        self.stopAction = self.menu.addAction('Stop')
        self.startAction = self.menu.addAction('Start')
        self.exitAction = self.menu.addAction('Exit')

        self.exitAction.triggered.connect(self.exit)
        self.settingsAction.triggered.connect(self.settings)
        self.changeSettingsAction.triggered.connect(self.change_setting)
        self.startAction.triggered.connect(self.start)
        self.stopAction.triggered.connect(self.stop)
        self.setContextMenu(self.menu)

    def exit(self):
        sys.exit()

    def settings(self):
        print('settings')
        #self.settings = Settings(screensize=self.screensize)

    def finished(self):
        print('finished')

    def change_setting(self):
        print('change_setting')
        #self.changeSettingsAction.triggered.connect(lambda: self.worker.change_settings(self.city, self.period))

    def start(self):
        print('start')
        #self.update()

    def stop(self):
        print('stop')

    @pyqtSlot(int)
    def setIcon(self, temp):
        icon = QtGui.QIcon(f"resources\\{temp}.bmp")
        super(SystemTrayIcon, self).setIcon(icon)
        self.setToolTip(f'Now is {temp}')
'''
    def update(self, city, period):
        self.thread = QThread()
        self.worker = Worker(city, period)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.temp.connect(self.setIcon)
        self.worker.finished.connect(self.finished)
        self.stopAction.triggered.connect(lambda: self.worker.stop())
        self.startAction.triggered.connect(lambda: self.worker.start())
        self.thread.start()
'''


class Settings(QtWidgets.QMainWindow):
    def __init__(self, screensize):
        super().__init__()
        self.setWindowTitle("Weather Desktop Tray - Settings")
        self.width = 400
        self.height = 400
        self.setGeometry(screensize[0]-self.width-20, screensize[1]-self.height-20, self.width, self.height)

        self.edit_city = QtWidgets.QLineEdit(self)
        self.edit_city.setText('Moscow, ru')
        self.listCities = QtWidgets.QListWidget(self)
        self.listCities.resize(100, 200)
        self.listCities.insertItem(0, 'Chicago, us')
        self.listCities.insertItem(1, 'Paris, fr')
        self.listCities.clicked.connect(self.click_list_cities)
        self.edit_city.move(150, 20)
        self.edit_city.resize(280, 40)

        self.button_save = QtWidgets.QPushButton("Save", self)
        self.button_save.move(self.width-150, self.height-100)
        self.button_save.clicked.connect(self.save)
        self.button_cancel = QtWidgets.QPushButton("Cancel", self)
        self.button_cancel.move(50, self.height - 100)
        self.button_cancel.clicked.connect(self.cancel)
        self.show()

    def click_list_cities(self, index):
        item = self.listCities.currentItem()
        text = item.text()
        self.edit_city.setText(text)

    def save(self):
        global city
        city = self.edit_city.text()
        print('save')

    def cancel(self):
        print('cancel')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Main(app)
    sys.exit(app.exec_())
