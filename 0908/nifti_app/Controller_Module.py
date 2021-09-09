from PyQt5.QtWidgets import QFileDialog


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
