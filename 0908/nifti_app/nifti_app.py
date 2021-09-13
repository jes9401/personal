from PyQt5.QtWidgets import QApplication
from main_window_module import MainWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MainWindow()
    form.setWindowTitle('nifti_app')
    form.setFixedWidth(960)
    form.setFixedHeight(480)
    form.show()
    app.exec_()
