"""
weather app for desktop by Sergey Meshkov
"""
import datetime
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
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

    def update_settings(self):
        self.city = settings.read_config('settings.ini', 'city')
        self.period = int(settings.read_config('settings.ini', 'period'))
        self.apikey = settings.read_config('settings.ini', 'apikey')
        self.cities = set(settings.read_config('settings.ini', 'cities').split(';'))

    def createWorkerThread(self):
        # Setup the worker object and the worker_thread.
        self.worker = Worker(self.city, self.period, self.apikey)
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()
        self.worker.temp.connect(self.gui.setIcon)
        self.gui.startAction.triggered.connect(self.worker.startWork)

    def _connectSignals(self):
        self.gui.stopAction.triggered.connect(self.forceWorkerReset)
        self.gui.settings.button_save.clicked.connect(self.forceWorkerReset)

        self.temp.connect(self.gui.setIcon)
        self.parent().aboutToQuit.connect(self.forceWorkerQuit)

    def forceWorkerReset(self):
        if self.worker_thread.isRunning():
            print('Terminating thread.')
            self.worker_thread.terminate()
            print('Waiting for thread termination.')
            self.worker_thread.wait()
            print('building new working object.')
            self.update_settings()
            self.createWorkerThread()
            self.gui.startAction.trigger()

    def forceWorkerQuit(self):
        if self.worker_thread.isRunning():
            self.worker_thread.terminate()
            self.worker_thread.wait()


class Worker(QObject):
    temp = pyqtSignal(int)

    def __init__(self, city, period, apikey, parent=None):
        super(self.__class__, self).__init__(parent)
        self.city = city
        self.period = period
        self.apikey = apikey

    @pyqtSlot()
    def startWork(self):
        print('Start work Worker')
        while True:
            self.temp.emit(weather.get_current_temp(city=self.city, apikey=self.apikey))
            print(f'sleeping {self.period} seconds')
            time.sleep(self.period)

    def change_settings(self, city, period):
        pass


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        user32 = ctypes.windll.user32
        self.screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

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

        self.settings = Settings(screensize=self.screensize)

    def show(self):
        QtWidgets.QSystemTrayIcon.show(self)
        self.startAction.trigger()

    def exit(self):
        sys.exit()

    def settings(self):
        print('settings')
        #self.settings = Settings(screensize=self.screensize)
        self.settings.show()

    def finished(self):
        print('finished')

    def start(self):
        print('start')
        #self.update()

    def stop(self):
        print('stop')

    @pyqtSlot(int)
    def setIcon(self, temp):
        city = settings.read_config('settings.ini', 'city')
        time_str = datetime.datetime.now().strftime('%H:%M:%S')
        icon = QtGui.QIcon(f"resources\\{temp}.bmp")
        super(SystemTrayIcon, self).setIcon(icon)
        self.setToolTip(f'At {time_str} in {city} is {temp} celsius')


class Settings(QtWidgets.QWidget):
    def __init__(self, screensize):
        super().__init__()

        self.icon = QtGui.QIcon(f"resources\\settings-svgrepo-com.svg")
        self.setWindowIcon(self.icon)
        self.setWindowTitle("Weather Desktop Tray - Settings")
        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(10)

        self.edit_city = QtWidgets.QLineEdit(self)
        self.label_city = QtWidgets.QLabel("Current city", self)

        self.edit_apikey = QtWidgets.QLineEdit(self)
        self.label_apikey = QtWidgets.QLabel("Your api-key", self)

        self.listCities = QtWidgets.QListWidget(self)

        self.label_period = QtWidgets.QLabel("Period of update(secs)", self)
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
        self.setGeometry(screensize[0] - self.width - 30, screensize[1] - self.height - 40, self.width, self.height)

        #self.show()

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
