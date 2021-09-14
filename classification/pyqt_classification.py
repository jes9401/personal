import sys
from PyQt5.QtWidgets import *
import torch
from monai.networks.nets import DenseNet121
from monai.transforms import (
    AddChannel,
    Compose,
    LoadImage,
    ScaleIntensity,
    EnsureType,
)


# model predict
def get_result(file_name):
    # class 이름 리스트에 저장
    # DATA_DIR = os.path.join("MedNIST")
    # class_names = sorted(x for x in os.listdir(DATA_DIR)
    #                      if os.path.isdir(os.path.join(DATA_DIR, x)))
    class_names = ['AbdomenCT', 'BreastMRI', 'CXR', 'ChestCT', 'Hand', 'HeadCT']
    # 입력받은 파일 경로 저장, test_y는 필요 없기 때문에 임의로 0 지정
    test_x = [file_name]
    test_y = [0]
    val_transforms = Compose(
        [LoadImage(image_only=True), AddChannel(), ScaleIntensity(), EnsureType()])

    class MedNISTDataset(torch.utils.data.Dataset):
        def __init__(self, image_files, labels, transforms):
            self.image_files = image_files
            self.labels = labels
            self.transforms = transforms

        def __len__(self):
            return len(self.image_files)

        def __getitem__(self, index):
            return self.transforms(self.image_files[index]), self.labels[index]

    test_ds = MedNISTDataset(test_x, test_y, val_transforms)
    test_loader = torch.utils.data.DataLoader(
        test_ds, batch_size=300, num_workers=0)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = DenseNet121(spatial_dims=2, in_channels=1,
                        out_channels=6).to(device)
    model.load_state_dict(torch.load("C:\\Users\\NEUROPHET\\PycharmProjects\\pythonProject\\classification\\best_metric_model.pth"))
    model.eval()
    y_pred = []

    with torch.no_grad():
        for test_data in test_loader:
            test_images = test_data[0].to(device)
            pred = model(test_images).argmax(dim=1)
            for i in range(len(pred)):
                y_pred.append(pred[i].item())

    # 분류 모델 적용 결과 리턴
    result = class_names[y_pred[0]]
    return result


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.set_ui()

    def set_ui(self):
        self.setWindowTitle('Classification Test')

        # 행방향으로 위젯 배치하기 위한 레이아웃
        hbox1 = QHBoxLayout()
        self.label1 = QLabel("파일")
        self.tb1 = QTextBrowser()
        self.tb1.setFixedSize(300, 50)
        self.push_button = QPushButton('파일 선택')
        self.push_button.setFixedSize(100,25)
        self.push_button.clicked.connect(self.push_button_clicked)
        hbox1.addWidget(self.label1)
        hbox1.addStretch(1)
        hbox1.addWidget(self.tb1)
        hbox1.addWidget(self.push_button)

        hbox2 = QHBoxLayout()
        self.label2 = QLabel("사진")
        self.tb2 = QTextBrowser()
        self.tb2.setFixedSize(400, 80)
        hbox2.addWidget(self.label2)
        hbox2.addWidget(self.tb2)

        hbox3 = QHBoxLayout()
        self.label3 = QLabel("label")
        self.tb3 = QTextBrowser()
        self.tb3.setFixedSize(400, 50)
        hbox3.addWidget(self.label3)
        hbox3.addWidget(self.tb3)

        hbox4 = QHBoxLayout()
        self.btn1 = QPushButton('초기화')
        self.btn1.clicked.connect(self.reset)
        self.btn2 = QPushButton('시작')
        self.btn2.clicked.connect(self.start)
        hbox4.addStretch(3)
        hbox4.addWidget(self.btn1)
        hbox4.addStretch(1)
        hbox4.addWidget(self.btn2)
        hbox4.addStretch(3)

        # 위젯을 수직 방향으로 나열하는 레이아웃
        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)

        self.setLayout(vbox)
        self.show()

    def push_button_clicked(self):
        self.file = QFileDialog.getOpenFileName(self)
        self.tb1.setText(self.file[0])
        self.tb2.setHtml("""<img src="{}"/>""".format(self.file[0]))
        self.tb3.clear()

    def reset(self):
        self.tb1.clear()
        self.tb2.clear()
        self.tb3.clear()
        self.file = ""

    def start(self):
        try:
            result = get_result(self.file[0])
            self.tb3.setText(result)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    app.exec_()