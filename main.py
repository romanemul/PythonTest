import sys
import traceback

from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QProgressBar, QListWidget
from PyQt5.QtCore import QRunnable, QObject, QThreadPool, pyqtSignal as Signal, pyqtSlot as Slot, pyqtSignal


class Signals(QObject):
        signal_one = Signal(int)
        signal_two = Signal(int)

class Worker(QRunnable):
    def __init__(self, n, *args, **kwargs):
        super(Worker, self).__init__()
        self.n = n
        self.signals = Signals()

    @Slot()
    def run(self):
        print("Thread start")
        self.signals.signal_one.emit(self.n)
        self.signals.signal_two.emit(self.n)
#
#
class MainWindow(QMainWindow):
    def __init__(self, parent=None, *args, **kwargs):
        # super(MainWindow, self).__init__(*args, **kwargs)
        super().__init__(parent)
        self.setWindowTitle('QThreadPool Demo')

        self.job_count = 10
        self.comleted_jobs = []

        widget = QWidget()
        widget.setLayout(QGridLayout())
        self.setCentralWidget(widget)

        self.btn_start = QPushButton('Start', clicked=self.start_jobs)
        self.progress_bar = QProgressBar(minimum=0, maximum=self.job_count)
        self.list = QListWidget()

        widget.layout().addWidget(self.list, 0, 0, 1, 2)
        widget.layout().addWidget(self.progress_bar, 1, 0)
        widget.layout().addWidget(self.btn_start, 1, 1)

        self.show()
#
    def start_jobs(self):
        self.restart()
        pool = QThreadPool.globalInstance()
        for i in range(1, self.job_count + 1):
            worker = Worker(i)
            worker.signals.signal_one.connect(self.complete)
            worker.signals.signal_two.connect(self.start)
            pool.start(worker)
#
    def restart(self):
        self.progress_bar.setValue(0)
        self.comleted_jobs = []
        self.btn_start.setEnabled(False)
#
    def start(self, n):
        self.list.addItem(f'Job #{n} started...')

    def complete(self, n):
        self.list.addItem(f'Job #{n} completed.')
        self.comleted_jobs.append(n)
        self.progress_bar.setValue(len(self.comleted_jobs))

        if len(self.comleted_jobs) == self.job_count:
            self.btn_start.setEnabled(True)


app = QApplication([])
window = MainWindow()
app.exec_()
