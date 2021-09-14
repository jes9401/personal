import nibabel as nib
from PIL import Image
from PyQt5 import QtCore, QtGui


class Model(QtCore.QObject):
    def __init__(self):
        super().__init__()

    # 파일을 선택하면 해당 파일의 x, y, z축 0번째 image를
    # Qimage 객체로 생성 후 반환
    def get_image(self, image_path):
        self.data = nib.load(image_path)
        # size는 3개의 슬라이더 값 설정에 사용
        size = list(self.data.header['dim'][1:4])
        x_qim = self.show_image(0, "x")
        y_qim = self.show_image(0, "y")
        z_qim = self.show_image(0, "z")
        return x_qim, y_qim, z_qim, size

    # 슬라이더의 값(number), 축(dim) 값을 이용해 Qimage 생성
    def show_image(self, number, dim):
        if dim == "x":
            image = self.data.dataobj[number, :, :]
        elif dim == "y":
            image = self.data.dataobj[:, number, :]
        else:
            image = self.data.dataobj[:, :, number]
        # numpy array 형태의 데이터를 Image 객체로 변환
        image = Image.fromarray(image)
        image = image.convert("RGBA")
        # 좌측으로 90도 회전
        image = image.transpose(Image.ROTATE_90)
        # byte 형태로 변환 => QImage 객체 생성할 때 파라미터 값
        image_data = image.tobytes("raw", "RGBA")
        q_image = QtGui.QImage(image_data, image.size[0], image.size[1], QtGui.QImage.Format_ARGB32)
        return q_image
    