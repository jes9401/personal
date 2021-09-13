from PyQt5 import QtGui


class View():
    def __init__(self, main_window):
        self.main_window = main_window

    # 지정한 인덱스의 이미지를 화면에 출력하는 함수
    def print_image(self, image, dim):
        # 파일 선택을 완료하면 hide 해놨던 위젯들을 보이게 변경
        self.main_window.image_select_slider_x.show()
        self.main_window.image_select_slider_y.show()
        self.main_window.image_select_slider_z.show()
        self.main_window.image_section_x.show()
        self.main_window.image_section_y.show()
        self.main_window.image_section_z.show()
        # 입력받은 dim 값에 따라 해당 부분 이미지 출력
        if dim == "x":
            pix = QtGui.QPixmap(image)
            self.main_window.image_section_x.setPixmap(pix)
        elif dim == "y":
            pix = QtGui.QPixmap(image)
            self.main_window.image_section_y.setPixmap(pix)
        else:
            pix = QtGui.QPixmap(image)
            self.main_window.image_section_z.setPixmap(pix)

    # 파일 정보 출력하는 함수
    def print_image_info(self):
        # 파일 선택시 저장해둔 data를 변수에 저장
        temp = self.main_window.model.data
        spacing = list(temp.header['pixdim'])[:3]
        self.main_window.image_info.show()
        self.main_window.image_info.setText("")
        self.main_window.image_info.append("shape => {}".format(temp.shape))
        self.main_window.image_info.append("\nimage size => ")
        self.main_window.image_info.append("\tx축 기준 {}".format(temp.shape[1:]))
        self.main_window.image_info.append("\ty축 기준 ({}, {})".format(temp.shape[0], temp.shape[-1]))
        self.main_window.image_info.append("\tz축 기준 {}".format(temp.shape[:-1]))
        self.main_window.image_info.append("\nspacing => {}".format(spacing))

