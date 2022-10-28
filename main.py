import sys
import traceback

import cv2
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QProgressBar, QListWidget
from PyQt5.QtCore import QRunnable, QObject, QThreadPool, pyqtSignal as Signal, pyqtSlot as Slot, pyqtSignal


class Signals(QObject):
        signal_one = Signal(int)
        signal_two = Signal(int)
        signal_three = Signal()

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
        worker = Worker(10)
        worker.signals.signal_one.connect(self.run_cam)
        pool.start(worker)
        # for i in range(1, self.job_count + 1):
        #     worker = Worker(i)
        #     worker.signals.signal_one.connect(self.complete)
        #     worker.signals.signal_two.connect(self.start)
        #     pool.start(worker)

    def run_cam(self):
        vid = cv2.VideoCapture(0)

        while (True):

            # Capture the video frame
            # by frame
            ret, frame = vid.read()

            # Display the resulting frame
            cv2.imshow('frame', frame)

            # the 'q' button is set as the
            # quitting button you may use any
            # desired button of your choice
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # After the loop release the cap object
        vid.release()
        # Destroy all the windows
        cv2.destroyAllWindows()
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



import time

import sys


# class Parent():
#     def __init__(self, sex):
#         self.age = 20
#         self.sex = sex
#
#     def add(self, first, second):
#         return first + second
#
# class Child(Parent):
#     def __init__(self, sex):
#         super(Child, self).__init__(sex)
#         self.age = self.age
#
#     def add(self, first, second, third):
#         return first + second + third#
#
# class OtherChild(Child):
#     def __init__(self):
#         def add(self, one, two , three, four):
#             return one + two + three + four
#
# p = Parent("s")
# print(p.age)
# print(p.sex)
#
# c = Child("F")
#
# print(c.age)
# s = c.add(3, 5, 5)
# super(Child, c).add(11,2)
# print(s)
#
#
# other = OtherChild
# print(c.sex)
# # print(other.age)