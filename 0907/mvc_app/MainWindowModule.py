from PyQt5.QtWidgets import *
from ModelModule import Model
from View1Module import View1
from View2Module import View2
from View3Module import View3
from ControllerModule import Controller


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.model = Model()
        self.view1 = View1(self)
        self.view2 = View2(self)
        self.view3 = View3(self)
        self.controller = Controller(self)

        tabs = QTabWidget()
        tabs.addTab(self.view1.tab1(), '총 목록')
        tabs.addTab(self.view2.tab2(), '검색')
        tabs.addTab(self.view3.tab3(), '고객 관리')

        vbox = QVBoxLayout()
        vbox.addWidget(tabs)
        self.setLayout(vbox)
