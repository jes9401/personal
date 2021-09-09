from PyQt5 import QtGui


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
        temp = self.main_window.model.data
        self.main_window.image_info.show()
        self.main_window.image_info.setText(" ")
        self.main_window.image_info.append("shape => {}\n".format(temp.shape))
        self.main_window.image_info.append("image size => ")
        self.main_window.image_info.append("\tx축 기준 {}".format(temp.shape[1:]))
        self.main_window.image_info.append("\ty축 기준 ({}, {})".format(temp.shape[0], temp.shape[-1]))
        self.main_window.image_info.append("\tz축 기준 {}".format(temp.shape[:-1]))
        # self.main_window.image_info.append("총 이미지 수 => {}".format(str(sum(temp.shape))))
        self.main_window.image_info.append("\npixdim => {}".format(temp.header['pixdim']))
