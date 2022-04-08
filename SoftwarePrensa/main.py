from monitor import Monitor
from PyQt5 import QtWidgets
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    monitor = Monitor()
    monitor.show()
    app.exec_()
