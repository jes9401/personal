from PyQt5.QtWidgets import *
from functools import partial


class Tab2View():
    def __init__(self, main_window):
        self.main_window = main_window
    
    # 2번째 탭 구현(검색)
    def tab2(self):
        tab2 = QWidget()
        self.main_window.line_edit = QLineEdit()
        search_button = QPushButton("검색")
        search_button.clicked.connect(self.main_window.controller.search)
        self.main_window.table2 = QTableWidget()
        self.main_window.table2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        hlabels = ["고객 이름", "전화 번호", "등급", "거래 내역"]
        self.main_window.model.set_header(self.main_window.table2, hlabels)
        tab2_layout_h = QHBoxLayout()
        tab2_layout_h.addWidget(self.main_window.line_edit)
        tab2_layout_h.addWidget(search_button)
        tab2_layout = QVBoxLayout()
        tab2_layout.addLayout(tab2_layout_h)
        tab2_layout.addWidget(self.main_window.table2)
        tab2.setLayout(tab2_layout)
        return tab2

    # 검색 결과 화면
    def search_view(self, rows):
        for i in range(len(rows)):
            for j in range(3):
                self.main_window.table2.setItem(i, j, QTableWidgetItem(str(rows[i][j])))
            button = QPushButton("자세히")
            self.main_window.button_list.append(button)
            # 고객 상세 화면으로 연결
            self.main_window.button_list[i].clicked.connect(partial(self.main_window.controller.client_detail, rows[i][0]))
            self.main_window.table2.setCellWidget(i, 3, self.main_window.button_list[i])
