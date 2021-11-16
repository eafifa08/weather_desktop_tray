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
        self.update_settings()
        self.w = QtWidgets.QWidget()
        self.gui = SystemTrayIcon(QtGui.QIcon("resources\\thermometer.png"), self.w)
        self.createWorkerThread()
        self._connectSignals()
        self.gui.show()
        self.gui.startAction.toggle()

    def update_settings(self):
        self.city = settings.read_config('settings.ini', 'city')
        self.period = int(settings.read_config('settings.ini', 'period'))
        self.cities = set(settings.read_config('settings.ini', 'cities').split(';'))

    def createWorkerThread(self):
        # Setup the worker object and the worker_thread.
        self.worker = Worker(self.city, self.period)
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()
        #self.worker_thread.started.connect(self.worker.run)
        self.worker.temp.connect(self.gui.setIcon)
        self.gui.startAction.triggered.connect(self.worker.startWork)

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
            #self.temp.emit('Idle.')
            print('building new working object.')
            self.update_settings()
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
    def startWork(self):
        while True:
            self.temp.emit(weather.get_current_temp(self.city))
            #self.finished.emit(1)
            #self.my_continue = False
            print('sleep')
            time.sleep(self.period)

    def change_settings(self, city, period):
        pass


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
        self.stopAction = self.menu.addAction('Stop')
        self.startAction = self.menu.addAction('Start')
        self.exitAction = self.menu.addAction('Exit')

        self.exitAction.triggered.connect(self.exit)
        self.settingsAction.triggered.connect(self.settings)
        self.startAction.triggered.connect(self.start)
        self.stopAction.triggered.connect(self.stop)
        self.setContextMenu(self.menu)

    def show(self):
        QtWidgets.QSystemTrayIcon.show(self)
        self.startAction.trigger()

    def exit(self):
        sys.exit()

    def settings(self):
        print('settings')
        self.settings = Settings(screensize=self.screensize)

    def finished(self):
        print('finished')

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


class Settings(QtWidgets.QWidget):
    def __init__(self, screensize):
        super().__init__()
        self.setWindowTitle("Weather Desktop Tray - Settings")
        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(10)

        self.edit_city = QtWidgets.QLineEdit(self)
        self.label_city = QtWidgets.QLabel("Current city", self)

        self.edit_apikey = QtWidgets.QLineEdit(self)
        self.label_apikey = QtWidgets.QLabel("Your api-key", self)

        self.listCities = QtWidgets.QListWidget(self)

        self.label_period = QtWidgets.QLabel("Period of update", self)
        self.onlyInt = QtGui.QIntValidator(1, 9999, self)
        self.edit_period = QtWidgets.QLineEdit(self)
        self.edit_period.setValidator(self.onlyInt)

        self.fillSettings()
        self.listCities.clicked.connect(self.click_list_cities)
        self.button_save = QtWidgets.QPushButton("Save", self)
        self.button_save.clicked.connect(self.save)
        self.button_cancel = QtWidgets.QPushButton("Cancel", self)
        self.button_cancel.clicked.connect(self.cancel)

        self.grid.addWidget(self.listCities, 0, 0, 1, 2)
        self.grid.addWidget(self.label_city, 1, 0)
        self.grid.addWidget(self.edit_city, 1, 1)
        self.grid.addWidget(self.label_period, 2, 0)
        self.grid.addWidget(self.edit_period, 2, 1)
        self.grid.addWidget(self.label_apikey, 3, 0)
        self.grid.addWidget(self.edit_apikey, 3, 1)
        self.grid.addWidget(self.button_save, 4, 0)
        self.grid.addWidget(self.button_cancel, 4, 1)
        self.setLayout(self.grid)

        self.width = 400
        self.height = 400
        self.setGeometry(screensize[0] - self.width - 20, screensize[1] - self.height - 20, self.width, self.height)

        self.show()

    def fillSettings(self):
        cities = settings.read_config('settings.ini', 'cities').split(';')
        self.listCities.clear()
        for tempCity in cities:
            self.listCities.addItem(tempCity)
        self.edit_city.setText(settings.read_config('settings.ini', 'city'))
        self.edit_period.setText(settings.read_config('settings.ini', 'period'))
        self.edit_apikey.setText(settings.read_config('settings.ini', 'apikey'))

    def click_list_cities(self, index):
        item = self.listCities.currentItem()
        text = item.text()
        self.edit_city.setText(text)

    def save(self):
        #self.city = settings.read_config('settings.ini', 'city')
        #self.period = int(settings.read_config('settings.ini', 'period'))
        #global city
        city = self.edit_city.text()
        period = self.edit_period.text()
        apikey = self.edit_apikey.text()
        cities = settings.read_config('settings.ini', 'cities').split(';')
        cities.append(city)
        cities = set(cities)
        cities = list(cities)
        cities.sort()
        cities = ";".join(cities)
        settings.write_config('settings.ini', 'cities', cities)
        settings.write_config('settings.ini', 'city', city)
        settings.write_config('settings.ini', 'period', period)
        settings.write_config('settings.ini', 'apikey', apikey)
        self.fillSettings()
        print('save')

    def cancel(self):
        self.close()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    main = Main(app)
    sys.exit(app.exec_())
