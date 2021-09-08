import nibabel as nib
import sys
import os
import pymysql
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from functools import partial
import numpy as np
from PIL import Image
from PIL.ImageQt import ImageQt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.model = Model()
        self.view = View(self)
        self.controller = Controller(self)

        file_layout = QHBoxLayout()
        file_choice_button = QPushButton("파일 선택")
        file_choice_button.clicked.connect(self.controller.file_choice)
        file_layout.addStretch(5)
        file_layout.addWidget(file_choice_button)

        image_select_layout = QHBoxLayout()
        image_select_slider = QSlider(Qt.Horizontal)
        # image_select_slider.move(30, 30)
        # image_select_slider.setRange(0, 50)
        image_select_button = QPushButton("선택")
        image_select_button.clicked.connect(self.controller.image_select)
        image_select_layout.addWidget(image_select_slider)
        image_select_layout.addWidget(image_select_button)

        self.image_section = QLabel("대기")
        image_section_layout = QVBoxLayout()
        image_section_layout.addWidget(self.image_section)

        vbox = QVBoxLayout()
        vbox.addLayout(file_layout)
        vbox.addLayout(image_select_layout)
        vbox.addLayout(image_section_layout)
        self.setLayout(vbox)


class Model(QtCore.QObject):
    def __init__(self):
        super().__init__()

    # QPixmap 사용
    # 원래 dtype은 "<f8" 인데 numpy의 실수형은 float16 이상이라 uint8로 변환했음
    # => 그래서 색이 좀 깨지는 현상이 발생하는데 어떻게 할지 고민중..
    def get_image(self, image_path):
        data = nib.load(image_path)
        image_data = data.get_fdata()
        # image = Image.fromarray(image_data[0])
        image = image_data[80]
        height, width = image.shape
        try:
            print(np.require(image, np.float16, 'C').dtype)
            qim = QtGui.QImage(np.require(image, np.uint8, 'C') , width, height, width, QtGui.QImage.Format_Indexed8)
        except Exception as e:
            print(e)
        return qim


class View():
    def __init__(self, main_window):
        self.main_window = main_window

    def print_image(self, image):
        try:
            pix = QtGui.QPixmap(image)
        except Exception as e:
            print(e)
        try:
            self.main_window.image_section.setPixmap(pix)
        except Exception as e:
            print(e)


class Controller():
    def __init__(self, main_window):
        self.main_window = main_window

    def file_choice(self):
        self.file = QFileDialog.getOpenFileName(self.main_window)
        qim = self.main_window.model.get_image(self.file[0])
        self.main_window.view.print_image(qim)

    def image_select(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MainWindow()
    form.setWindowTitle('nifti_app')
    form.setFixedWidth(640)
    form.setFixedHeight(480)
    form.show()
    app.exec_()


