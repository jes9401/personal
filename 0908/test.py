import nibabel as nib
import sys
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from functools import partial
from PIL import Image


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.model = Model()
        self.view = View(self)
        self.controller = Controller(self)

        file_layout = QHBoxLayout()
        self.file_name_label = QLabel()
        file_choice_button = QPushButton("파일 선택")
        file_choice_button.clicked.connect(self.controller.file_choice)
        file_layout.addWidget(self.file_name_label)
        file_layout.addStretch(1)
        file_layout.addWidget(file_choice_button)

        x_layout = QHBoxLayout()
        self.image_select_slider_x = QSlider(Qt.Horizontal)
        self.image_select_slider_x.valueChanged.connect(self.controller.show_image_number)
        self.image_select_slider_x.valueChanged.connect(partial(self.controller.image_select, "x"))
        self.image_select_slider_x.hide()
        self.size_label_x = QLabel()
        x_layout.addWidget(self.image_select_slider_x)
        x_layout.addWidget(self.size_label_x)
        self.image_section_x = QLabel()
        self.image_section_x.setAlignment(Qt.AlignCenter)
        self.image_section_x.hide()
        x_layout_2 = QVBoxLayout()
        x_layout_2.addLayout(x_layout)
        x_layout_2.addWidget(self.image_section_x)

        y_layout = QHBoxLayout()
        self.image_select_slider_y = QSlider(Qt.Horizontal)
        self.image_select_slider_y.valueChanged.connect(self.controller.show_image_number)
        self.image_select_slider_y.valueChanged.connect(partial(self.controller.image_select, "y"))
        self.image_select_slider_y.hide()
        self.size_label_y = QLabel()
        y_layout.addWidget(self.image_select_slider_y)
        y_layout.addWidget(self.size_label_y)
        self.image_section_y = QLabel()
        self.image_section_y.setAlignment(Qt.AlignCenter)
        self.image_section_y.hide()
        y_layout_2 = QVBoxLayout()
        y_layout_2.addLayout(y_layout)
        y_layout_2.addStretch(1)
        y_layout_2.addWidget(self.image_section_y)

        z_layout = QHBoxLayout()
        self.image_select_slider_z = QSlider(Qt.Horizontal)
        self.image_select_slider_z.valueChanged.connect(self.controller.show_image_number)
        self.image_select_slider_z.valueChanged.connect(partial(self.controller.image_select, "z"))
        self.image_select_slider_z.hide()
        self.size_label_z = QLabel()
        z_layout.addWidget(self.image_select_slider_z)
        z_layout.addWidget(self.size_label_z)
        self.image_section_z = QLabel()
        self.image_section_z.setAlignment(Qt.AlignCenter)
        self.image_section_z.hide()
        z_layout_2 = QVBoxLayout()
        z_layout_2.addLayout(z_layout)
        z_layout_2.addStretch(1)
        z_layout_2.addWidget(self.image_section_z)

        image_section_layout = QHBoxLayout()
        image_section_layout.addLayout(x_layout_2)
        image_section_layout.addLayout(y_layout_2)
        image_section_layout.addLayout(z_layout_2)

        image_info_layout = QVBoxLayout()
        self.image_info = QTextBrowser()
        self.image_info.hide()
        image_info_layout.addWidget(self.image_info)

        vbox = QVBoxLayout()
        vbox.addLayout(file_layout)
        vbox.addLayout(image_section_layout)
        vbox.addLayout(image_info_layout)
        self.setLayout(vbox)


class Model(QtCore.QObject):
    def __init__(self):
        super().__init__()

    def get_image(self, image_path):
        global data
        data = nib.load(image_path)
        size = list(data.header['dim'][1:4])
        x_qim = self.show_image(0, "x")
        y_qim = self.show_image(0, "y")
        z_qim = self.show_image(0, "z")

        return x_qim, y_qim, z_qim, size

    def show_image(self, number, dim):
        if dim == "x":
            image = data.dataobj[number, :, :]
        elif dim == "y":
            image = data.dataobj[:, number, :]
        else:
            image = data.dataobj[:, :, number]
        # image = Image.fromarray(image)
        # image = image.convert("RGB")
        # r, g, b = image.split()
        # im = Image.merge("RGB", (b, g, r))
        # im2 = im.convert("RGBA")
        # im_data = im2.tobytes("raw", "RGBA")
        # qim = QtGui.QImage(im_data, im.size[0], im.size[1], QtGui.QImage.Format_ARGB32)

        image = Image.fromarray(image)
        image = image.transpose(Image.ROTATE_90)
        image = image.convert("RGBA")
        im_data = image.tobytes("raw", "RGBA")
        qim = QtGui.QImage(im_data, image.size[0], image.size[1], QtGui.QImage.Format_ARGB32)
        return qim


class View():
    def __init__(self, main_window):
        self.main_window = main_window

    def print_image(self, image, dim):
        self.main_window.image_select_slider_x.show()
        self.main_window.image_select_slider_y.show()
        self.main_window.image_select_slider_z.show()
        self.main_window.image_section_x.show()
        self.main_window.image_section_y.show()
        self.main_window.image_section_z.show()
        if dim == "x":
            pix = QtGui.QPixmap(image)
            self.main_window.image_section_x.setPixmap(pix)
        elif dim == "y":
            pix = QtGui.QPixmap(image)
            self.main_window.image_section_y.setPixmap(pix)
        else:
            pix = QtGui.QPixmap(image)
            self.main_window.image_section_z.setPixmap(pix)

    def print_image_info(self):
        self.main_window.image_info.show()
        self.main_window.image_info.setText(" ")
        self.main_window.image_info.append("shape => {}\n".format(data.shape))
        self.main_window.image_info.append("image size => ")
        self.main_window.image_info.append("\tx축 기준 {}".format(data.shape[1:]))
        self.main_window.image_info.append("\ty축 기준 ({}, {})".format(data.shape[0],data.shape[-1]))
        self.main_window.image_info.append("\tz축 기준 {}".format(data.shape[:-1]))
        # self.main_window.image_info.append("총 이미지 수 => {}".format(str(sum(data.shape))))
        self.main_window.image_info.append("\npixdim => {}".format(str(data.header['pixdim'])))


class Controller():
    def __init__(self, main_window):
        self.main_window = main_window

    def file_choice(self):
        self.file = QFileDialog.getOpenFileName(self.main_window)
        self.main_window.file_name_label.setText(self.file[0].split("/")[-1])
        x_qim, y_qim, z_qim, size = self.main_window.model.get_image(self.file[0])
        self.main_window.image_select_slider_x.setRange(0, size[0] - 1)
        self.main_window.image_select_slider_x.setValue(0)
        self.main_window.image_select_slider_y.setRange(0, size[1] - 1)
        self.main_window.image_select_slider_y.setValue(0)
        self.main_window.image_select_slider_z.setRange(0, size[2] - 1)
        self.main_window.image_select_slider_z.setValue(0)
        self.show_image_number()
        self.main_window.view.print_image(x_qim, "x")
        self.main_window.view.print_image(y_qim, "y")
        self.main_window.view.print_image(z_qim, "z")
        self.main_window.view.print_image_info()

    def image_select(self, dim):
        if dim == "x":
            number = self.main_window.image_select_slider_x.value()
        elif dim == "y":
            number = self.main_window.image_select_slider_y.value()
        else:
            number = self.main_window.image_select_slider_z.value()
        qim = self.main_window.model.show_image(number, dim)
        self.main_window.view.print_image(qim, dim)

    def show_image_number(self):
        self.main_window.size_label_x.setText(str(self.main_window.image_select_slider_x.value()))
        self.main_window.size_label_y.setText(str(self.main_window.image_select_slider_y.value()))
        self.main_window.size_label_z.setText(str(self.main_window.image_select_slider_z.value()))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MainWindow()
    form.setWindowTitle('nifti_app')
    form.setFixedWidth(960)
    form.setFixedHeight(480)
    form.show()
    app.exec_()


