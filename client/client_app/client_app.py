import sys
from PyQt5.QtWidgets import *
from main_window_module import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MainWindow()
    form.setWindowTitle('MyApp')
    form.setFixedWidth(640)
    form.setFixedHeight(480)
    form.show()
    app.exec_()
