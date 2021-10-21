import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import time
import weather
import settings

# for getting screen-size
import ctypes

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
print(screensize)

city = settings.read_config('settings.ini', 'city')
period = int(settings.read_config('settings.ini', 'period'))


class Worker(QObject):
    finished = pyqtSignal()
    temp = pyqtSignal(int)

    def __init__(self, city, period):
        super(Worker, self).__init__()
        self.city = city
        self.period = period

    def run(self):
        while True:
            self.temp.emit(weather.get_current_temp(self.city))
            self.finished.emit()
            time.sleep(self.period)


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
        self.update(city, period)

    def exit(self):
        sys.exit()

    def settings(self):
        print('settings')
        self.next = Settings()

    def change_setting(self):
        self.thread.quit()
        self.update(city, period)

    def update(self, city, period):
        self.thread = QThread()
        self.worker = Worker(city, period)
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
        self.setWindowTitle("Weather Desktop Tray - Settings")
        self.width = 400
        self.height = 400
        self.setGeometry(screensize[0]-self.width-20, screensize[1]-self.height-20, self.width, self.height)

        layout = QtWidgets.QHBoxLayout()
        window = QtWidgets.QWidget()
        self.setLayout(layout)
        self.radio_group = QtWidgets.QButtonGroup(self)
        self.radio_city = QtWidgets.QRadioButton("City name, Country short-name")
        self.radio_position = QtWidgets.QRadioButton("Latitude , Longitude")
        self.radio_group.addButton(self.radio_city)
        self.radio_group.addButton(self.radio_position)
        layout.addWidget(self.radio_city)
        layout.addWidget(self.radio_position)
        window.setLayout(layout)
        self.setCentralWidget(window)

        self.edit_city = QtWidgets.QLineEdit(self)
        #self.edit_city.move(20, 20)
        #self.edit_city.resize(280, 40)

        self.button_ok = QtWidgets.QPushButton("OK", self)
        self.button_ok.move(self.width-150, self.height-100)
        self.button_ok.clicked.connect(self.ok)
        self.button_cancel = QtWidgets.QPushButton("Cancel", self)
        self.button_cancel.move(50, self.height - 100)
        self.button_cancel.clicked.connect(self.cancel)
        self.show()

    def ok(self):
        print('ok')

    def cancel(self):
        print('cancel')


app = QtWidgets.QApplication(sys.argv)
w = QtWidgets.QWidget()
tray_icon = SystemTrayIcon(QtGui.QIcon("resources\\thermometer.png"), w)
tray_icon.show()
sys.exit(app.exec())
