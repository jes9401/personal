import nibabel as nib
from PIL import Image
from PyQt5 import QtCore, QtGui


class Model(QtCore.QObject):
    def __init__(self):
        super().__init__()

    def get_image(self, image_path):
        global data
        self.data = nib.load(image_path)
        size = list(self.data.header['dim'][1:4])
        x_qim = self.show_image(0, "x")
        y_qim = self.show_image(0, "y")
        z_qim = self.show_image(0, "z")

        return x_qim, y_qim, z_qim, size

    def show_image(self, number, dim):
        if dim == "x":
            image = self.data.dataobj[number, :, :]
        elif dim == "y":
            image = self.data.dataobj[:, number, :]
        else:
            image = self.data.dataobj[:, :, number]
        image = Image.fromarray(image)
        image = image.convert("RGB")
        image = image.transpose(Image.ROTATE_90)
        r, g, b = image.split()
        im = Image.merge("RGB", (b, g, r))
        im2 = im.convert("RGBA")
        im_data = im2.tobytes("raw", "RGBA")
        qim = QtGui.QImage(im_data, im.size[0], im.size[1], QtGui.QImage.Format_ARGB32)
        # image = Image.fromarray(image)
        # image = image.transpose(Image.ROTATE_90)
        # image = image.convert("RGBA")
        # im_data = image.tobytes("raw", "RGBA")
        # qim = QtGui.QImage(im_data, image.size[0], image.size[1], QtGui.QImage.Format_ARGB32)
        return qim