from PyQt5.QtWidgets import *
from ModelModule import Model
from Tab1_view_Module import Tab1_View
from Tab2_view_Module import Tab2_View
from Tab3_view_Module import Tab3_View
from ControllerModule import Controller


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.model = Model()
        self.tab1_view = Tab1_View(self)
        self.tab2_view = Tab2_View(self)
        self.tab3_view = Tab3_View(self)
        self.controller = Controller(self)

        tabs = QTabWidget()
        tabs.addTab(self.tab1_view.tab1(), '총 목록')
        tabs.addTab(self.tab2_view.tab2(), '검색')
        tabs.addTab(self.tab3_view.tab3(), '고객 관리')

        vbox = QVBoxLayout()
        vbox.addWidget(tabs)
        self.setLayout(vbox)
