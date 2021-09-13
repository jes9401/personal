from PyQt5.QtWidgets import QFileDialog


class Controller():
    def __init__(self, main_window):
        self.main_window = main_window

    # 파일 선택 버튼 눌렀을 때 수행하는 함수
    # 선택한 파일을 매개변수로 사용해 각 축의 0번째 이미지들을 받아온 뒤 view에 넘김
    def file_choice(self):
        self.file = QFileDialog.getOpenFileName(self.main_window)
        self.main_window.file_name_label.setText(self.file[0].split("/")[-1])
        # x, y, z 초기 이미지 생성
        x_qim, y_qim, z_qim, size = self.main_window.model.get_image(self.file[0])
        # 각각의 슬라이더 값 설정
        self.main_window.image_select_slider_x.setRange(0, size[0] - 1)
        self.main_window.image_select_slider_x.setValue(0)
        self.main_window.image_select_slider_y.setRange(0, size[1] - 1)
        self.main_window.image_select_slider_y.setValue(0)
        self.main_window.image_select_slider_z.setRange(0, size[2] - 1)
        self.main_window.image_select_slider_z.setValue(0)
        # 슬라이더 선택 값 출력
        self.show_image_number()
        # 생성한 x, y, z 이미지를 view에 넘김
        self.main_window.view.print_image(x_qim, "x")
        self.main_window.view.print_image(y_qim, "y")
        self.main_window.view.print_image(z_qim, "z")
        # 정보 출력
        self.main_window.view.print_image_info()

    # 슬라이더를 움직이면 해당 인덱스의 QImage 생성 및 반환
    def image_select(self, dim):
        # dim 값에 따라 슬라이더의 값 number 변수에 저장
        if dim == "x":
            number = self.main_window.image_select_slider_x.value()
        elif dim == "y":
            number = self.main_window.image_select_slider_y.value()
        else:
            number = self.main_window.image_select_slider_z.value()
        
        # QIage 객체 생성 후 view에 넘김
        q_image = self.main_window.model.show_image(number, dim)
        self.main_window.view.print_image(q_image, dim)

    # 슬라이더 값 출력 함수
    def show_image_number(self):
        self.main_window.size_label_x.setText(str(self.main_window.image_select_slider_x.value()))
        self.main_window.size_label_y.setText(str(self.main_window.image_select_slider_y.value()))
        self.main_window.size_label_z.setText(str(self.main_window.image_select_slider_z.value()))
