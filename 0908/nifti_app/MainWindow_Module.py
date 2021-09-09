from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from Controller_Module import Controller
from Model_Module import Model
from View_Module import View


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