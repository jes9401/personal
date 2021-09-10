import os
import sys

from PyQt5.QtWidgets import *


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle('Test')

        # 행방향으로 위젯 배치하기 위한 레이아웃
        hbox1 = QHBoxLayout()
        self.label1 = QLabel("파일")
        self.tb1 = QTextBrowser()
        self.tb1.setFixedSize(350, 25)
        self.pushButton = QPushButton('파일 선택')
        self.pushButton.clicked.connect(self.button_click)
        hbox1.addWidget(self.label1)
        hbox1.addWidget(self.tb1)
        hbox1.addWidget(self.pushButton)

        hbox2 = QHBoxLayout()
        self.label2 = QLabel("결과")
        hbox2.addWidget(self.label2)

        hbox3 = QHBoxLayout()
        self.label3 = QLabel("label")
        self.tb2 = QTextBrowser()
        self.tb2.setFixedSize(400, 50)
        hbox3.addWidget(self.label3)
        hbox3.addWidget(self.tb2)

        hbox4 = QHBoxLayout()
        self.label4 = QLabel("label count")
        self.tb3 = QTextBrowser()
        self.tb3.setFixedSize(400, 80)
        hbox4.addWidget(self.label4)
        hbox4.addWidget(self.tb3)

        hbox5 = QHBoxLayout()
        self.btn1 = QPushButton('초기화')
        self.btn1.clicked.connect(self.reset)
        self.btn2 = QPushButton('시작')
        self.btn2.clicked.connect(self.start)
        hbox5.addStretch(3)
        hbox5.addWidget(self.btn1)
        hbox5.addStretch(1)
        hbox5.addWidget(self.btn2)
        hbox5.addStretch(3)

        # 위젯을 수직 방향으로 나열하는 레이아웃
        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)

        self.setLayout(vbox)
        self.show()

    def button_click(self):
        self.fname = QFileDialog.getOpenFileName(self)
        self.tb1.setText(self.fname[0].split("/")[-1])

    def reset(self):
        self.tb1.clear()
        self.tb2.clear()
        self.tb3.clear()
        self.fname = ""

    def start(self):
        try:
            temp = os.popen('python C:\\Users\\NEUROPHET\\PycharmProjects\\pythonProject\\0831\\argparseTest.py --input_path '+self.fname[0]).read()
            tb2_data = temp.split('\n')[0]
            tb3_data = temp.split('\n')[1]
            self.tb2.setText(tb2_data)
            self.tb3.setText(tb3_data)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    app.exec_()
