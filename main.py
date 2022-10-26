from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import time

class Parent():
    def __init__(self, sex):
        self.age = 20
        self.sex = sex

    def add(self, first, second):
        return first + second

class Child(Parent):
    def __init__(self, sex):
        super(Child, self).__init__(sex)
        self.age = self.age

    def add(self, first, second, third):
        return first + second + third


class OtherChild(Child):
    def __init__(self):
        def add(self, one, two , three, four):
            return one + two + three + four

class Signals(QObject):
    def __init__(self):
        self.signa_one = Signals()

class Worker(QRunnable):
    def __init__(self, *args, **kwargs):
        super(Worker, self).__init__()
        self.args = args
        self.kwargs = kwargs

    'Worker thread'

    @pyqtSlot()
    def run(self):
        print("Thread start")


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.counter = 0

        layout = QVBoxLayout()

        self.l = QLabel("Start")
        b = QPushButton("DANGER!")
        b.pressed.connect(self.oh_no)

        c = QPushButton("?")
        c.pressed.connect(self.change_message)

        layout.addWidget(self.l)
        layout.addWidget(b)

        layout.addWidget(c)

        w = QWidget()
        w.setLayout(layout)

        self.setCentralWidget(w)

        self.show()

    def change_message(self):
        self.message = "OH NO"

    def oh_no(self):
        self.message = "Pressed"

        for n in range(100):
            time.sleep(0.1)
            self.l.setText(self.message)
            QApplication.processEvents()

app = QApplication([])
window = MainWindow()
app.exec_()


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