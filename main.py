import sys
import time
import psutil
import datetime
import ctypes
from ctypes import wintypes
from activity_control import Ui_MainWindow
import matplotlib.font_manager as font_manager
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, _, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        fig.set_facecolor('#2f2f2f')
        self.axes.set_facecolor('#2f2f2f')
        super(MplCanvas, self).__init__(fig)

class ActivityControl(QtWidgets.QMainWindow):
    def __init__(self):
        super(ActivityControl, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()
        self.timer = datetime.datetime.now()
        self.activity = {}

    def init_UI(self):
        self.sum = 0
        self.setWindowTitle('Экранное время')
        self.buttons = QVBoxLayout()
        self.buttons.addWidget(self.ui.radioButton)
        self.buttons.addWidget(self.ui.radioButton_2)
        self.buttons.addWidget(self.ui.radioButton_3)
        self.buttons.addWidget(self.ui.radioButton_4)
        self.buttons.addWidget(self.ui.radioButton_5)
        self.buttons.addWidget(self.ui.radioButton_6)
        for i in range(6):
            self.buttons.itemAt(i).widget().hide()
        self.ui.radioButton.clicked.connect(self.click_1)
        self.ui.radioButton_2.clicked.connect(self.click_2)
        self.ui.radioButton_3.clicked.connect(self.click_3)
        self.ui.radioButton_4.clicked.connect(self.click_4)
        self.ui.radioButton_5.clicked.connect(self.click_5)
        self.ui.radioButton_6.clicked.connect(self.click_6)
        self.ui.radioButton_7.clicked.connect(self.click_6)
        self.ui.radioButton_8.clicked.connect(self.click_6)
        self.ui.radioButton_9.clicked.connect(self.click_6)
        self.ui.radioButton_10.clicked.connect(self.click_6)
        self.ui.radioButton_10.setChecked(True)
        self.setLayout(self.buttons)
        self.times = QVBoxLayout()
        self.times.addWidget(self.ui.label)
        self.times.addWidget(self.ui.label_2)
        self.times.addWidget(self.ui.label_3)
        self.times.addWidget(self.ui.label_4)
        self.times.addWidget(self.ui.label_5)
        self.times.addWidget(self.ui.label_6)
        for i in range(6):
            self.times.itemAt(i).widget().hide()
        self.names = QVBoxLayout()
        self.names.addWidget(self.ui.label_7)
        self.names.addWidget(self.ui.label_8)
        self.names.addWidget(self.ui.label_9)
        self.names.addWidget(self.ui.label_10)
        self.names.addWidget(self.ui.label_11)
        self.names.addWidget(self.ui.label_12)
        for i in range(6):
            self.names.itemAt(i).widget().hide()
        self.progress = QVBoxLayout()
        self.progress.addWidget(self.ui.progressBar)
        self.progress.addWidget(self.ui.progressBar_2)
        self.progress.addWidget(self.ui.progressBar_3)
        self.progress.addWidget(self.ui.progressBar_4)
        self.progress.addWidget(self.ui.progressBar_5)
        self.progress.addWidget(self.ui.progressBar_6)
        for i in range(6):
            self.progress.itemAt(i).widget().hide()
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.sc.axes.set_prop_cycle('color', '#a2a2a2')
        self.sc.axes.pie((1,), labels=("",), wedgeprops=dict(width=0.5))
        prop = font_manager.FontProperties(family='Century Gothic', size=15)
        self.sc.axes.text(0, 0, datetime.timedelta(seconds=0), horizontalalignment='center', verticalalignment='center', fontproperties=prop, color='#a2a2a2')
        self.sc.draw()
        pid = wintypes.DWORD()
        active = ctypes.windll.user32.GetForegroundWindow()
        ctypes.windll.user32.GetWindowThreadProcessId(active, ctypes.byref(pid))
        pid = pid.value
        for item in psutil.process_iter():
            if pid == item.pid:
                self.cur = item.name()
        lay = QtWidgets.QHBoxLayout(self.ui.widget)
        lay.addWidget(self.sc)
        self.worker_thread = WorkerThread()
        self.worker_thread.progress_updated.connect(self.update_progress)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        self.worker_thread.start()
        self.worker = Worker()
        self.worker.progress.connect(self.loop)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.start()

    def click_1(self):
        self.activity[self.names.itemAt(0).widget().text()] = (self.activity[self.names.itemAt(0).widget().text()][0], not self.activity[self.names.itemAt(0).widget().text()][1])
        self.update_graph()

    def click_2(self):
        self.activity[self.names.itemAt(1).widget().text()] = (self.activity[self.names.itemAt(1).widget().text()][0], not self.activity[self.names.itemAt(1).widget().text()][1])
        self.update_graph()

    def click_3(self):
        self.activity[self.names.itemAt(2).widget().text()] = (self.activity[self.names.itemAt(2).widget().text()][0], not self.activity[self.names.itemAt(2).widget().text()][1])
        self.update_graph()

    def click_4(self):
        self.activity[self.names.itemAt(3).widget().text()] = (self.activity[self.names.itemAt(3).widget().text()][0], not self.activity[self.names.itemAt(3).widget().text()][1])
        self.update_graph()

    def click_5(self):
        self.activity[self.names.itemAt(4).widget().text()] = (self.activity[self.names.itemAt(4).widget().text()][0], not self.activity[self.names.itemAt(4).widget().text()][1])
        self.update_graph()

    def click_6(self):
        self.update_graph()

    def click_7(self):
        self.update_graph()

    def click_8(self):
        self.update_graph()

    def click_9(self):
        self.update_graph()

    def click_10(self):
        self.update_graph()

    def update_graph(self):
        self.sc.axes.clear()
        total = 0
        x = []
        durations = []
        for index, (act, duration) in enumerate(self.activity.items()):
            if index > 4:
                total += duration[0].total_seconds()
            elif duration[1]:
                durations.append(duration[0].total_seconds())
                x.append(act)
        if self.ui.radioButton_6.isChecked():
            durations.append(total)
            x.append("Прочее")
        prop = font_manager.FontProperties(family='Century Gothic', size=15)
        if self.ui.radioButton_10.isChecked():
            self.sc.axes.text(0, 0, datetime.timedelta(seconds=sum(map(int, durations))), horizontalalignment='center', verticalalignment='center', fontproperties=prop, color='#a2a2a2')
        if len(x) == 0:
            self.sc.axes.set_prop_cycle('color', '#a2a2a2')
            self.sc.axes.pie((1,), labels=("",), wedgeprops=dict(width=0.5))
            self.sc.draw()
            return
        colors = ['#00ffcf', '#00e5bb', '#00cca7', '#00b292', '#00997d', '#008068']
        self.sc.axes.set_prop_cycle('color', colors)
        pct = '%1.1f%%' if self.ui.radioButton_7.isChecked() else ''
        pie = self.sc.axes.pie(durations, labels=x, wedgeprops=dict(width=0.5), autopct=pct, pctdistance=0.70)
        prop = font_manager.FontProperties(family='Century Gothic', size=15)
        for text in pie[2]:
            text.set_fontproperties(prop)
            text.set_color('#2f2f2f')
        prop = font_manager.FontProperties(family='Century Gothic', size=12)
        for index, text in enumerate(pie[1]):
            text.set_fontproperties(prop)
            text.set_color(colors[index])
            if not self.ui.radioButton_9.isChecked():
                text.set_visible(False)
        if self.ui.radioButton_8.isChecked():
            legend = self.sc.axes.legend(pie[0], x, loc='best', prop={'family': 'Century Gothic', 'size': 12})
            legend.get_frame().set_facecolor('#a2a2a2')
        self.sc.draw()

    def loop(self):
        t = datetime.datetime.now()
        self.sum += (t - self.timer).total_seconds()
        if self.cur in self.activity:
            self.activity[self.cur] = (self.activity[self.cur][0] + (t - self.timer), self.activity[self.cur][1])
        else:
            if len(self.activity) < 6:
                self.names.itemAt(len(self.activity)).widget().show()
                self.times.itemAt(len(self.activity)).widget().show()
                self.buttons.itemAt(len(self.activity)).widget().show()
                self.progress.itemAt(len(self.activity)).widget().show()
            self.activity[self.cur] = (t - self.timer, False)
        self.timer = t
        self.activity = dict(sorted(self.activity.items(), key=lambda item: item[1][0], reverse=True))
        self.print()

    def update_progress(self, cur):
        self.cur = cur

    def print(self):
        total = datetime.timedelta()
        for index, (act, duration) in enumerate(self.activity.items()):
            seconds = duration[0].total_seconds()
            seconds = int(seconds)
            formatted_duration = datetime.timedelta(seconds=seconds)
            if index > 4:
                total += formatted_duration
                self.names.itemAt(5).widget().setText("Прочее")
                self.times.itemAt(5).widget().setText(str(total))
                self.progress.itemAt(5).widget().setValue(int(total.total_seconds() * 100 / self.sum))
            else:
                if duration[1]:
                    self.buttons.itemAt(index).widget().setChecked(True)
                else:
                    self.buttons.itemAt(index).widget().setChecked(False)
                self.names.itemAt(index).widget().setText(str(act))
                self.times.itemAt(index).widget().setText(str(formatted_duration))
                self.progress.itemAt(index).widget().setValue(int(duration[0].total_seconds() * 100 / self.sum))

class WorkerThread(QThread):
    progress_updated = pyqtSignal(str)
    def run(self):
        while True:
            time.sleep(0.01)
            pid = wintypes.DWORD()
            active = ctypes.windll.user32.GetForegroundWindow()
            ctypes.windll.user32.GetWindowThreadProcessId(active, ctypes.byref(pid))
            pid = pid.value
            for item in psutil.process_iter():
                if pid == item.pid:
                    cur = item.name()
                    self.progress_updated.emit(cur)

class Worker(QThread):
    progress = pyqtSignal(int)
    def run(self):
        while True:
            time.sleep(1)
            self.progress.emit(1)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = ActivityControl()
    application.show()
    sys.exit(app.exec())