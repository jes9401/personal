from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from functools import partial


class Tab3_View():
    def __init__(self, main_window):
        self.main_window = main_window

    # 3번째 탭 구현(고객 관리)
    def tab3(self):
        tab3 = QWidget()
        self.add_button = QPushButton("고객 등록")
        self.add_button.clicked.connect(self.main_window.tab3_view.client_info_create_view)
        self.main_window.table3 = QTableWidget()
        self.main_window.table3.setEditTriggers(QAbstractItemView.NoEditTriggers)
        hlabels = ["고객 이름", "수정", "삭제"]
        self.main_window.model.setHeader(self.main_window.table3, hlabels)
        tab3_layout_h = QHBoxLayout()
        tab3_layout_h.addStretch(5)
        tab3_layout_h.addWidget(self.add_button)
        tab3_layout = QVBoxLayout()
        tab3_layout.addLayout(tab3_layout_h)
        tab3_layout.addWidget(self.main_window.table3)
        tab3.setLayout(tab3_layout)
        tab3.actionEvent(self.main_window.controller.management())
        return tab3

    # 고객 관리 탭에 보이는 화면
    def management_view(self, rows):
        self.main_window.table3.setRowCount(len(rows))
        # 수정, 삭제 버튼을 저장할 리스트
        self.main_window.modify_button_list = []
        self.main_window.delete_button_list = []
        for i in range(len(rows)):
            self.main_window.table3.setItem(i, 0, QTableWidgetItem(str(rows[i][0])))
            modify_button = QPushButton("수정")
            delete_button = QPushButton("삭제")
            self.main_window.modify_button_list.append(modify_button)
            self.main_window.delete_button_list.append(delete_button)
            # 수정 기능, 삭제 기능을 진행하는 함수에 연결
            self.main_window.modify_button_list[i].clicked.connect(partial(self.main_window.controller.client_info_modify, rows[i][0]))
            self.main_window.delete_button_list[i].clicked.connect(partial(self.main_window.controller.client_info_delete, rows[i][0]))
            self.main_window.table3.setCellWidget(i, 1, self.main_window.modify_button_list[i])
            self.main_window.table3.setCellWidget(i, 2, self.main_window.delete_button_list[i])

    # 고객 등록 화면
    def client_info_create_view(self):
        self.main_window.create_dialog = QDialog()
        self.main_window.create_dialog.setFixedWidth(320)
        self.main_window.create_dialog.setFixedHeight(240)
        self.main_window.create_dialog.setWindowTitle("고객 등록")
        self.main_window.create_dialog.setWindowModality(Qt.ApplicationModal)

        create_h_layout1 = QHBoxLayout()
        label1 = QLabel("이름")
        self.main_window.create_line_edit1 = QLineEdit()
        create_h_layout1.addWidget(label1)
        create_h_layout1.addWidget(self.main_window.create_line_edit1)

        create_h_layout2 = QHBoxLayout()
        label2 = QLabel("등급")
        self.main_window.create_line_edit2 = QLineEdit()
        create_h_layout2.addWidget(label2)
        create_h_layout2.addWidget(self.main_window.create_line_edit2)

        create_h_layout3 = QHBoxLayout()
        label3 = QLabel("번호")
        self.main_window.create_line_edit3 = QLineEdit()
        create_h_layout3.addWidget(label3)
        create_h_layout3.addWidget(self.main_window.create_line_edit3)
        create_h_layout4 = QHBoxLayout()
        # "등록" 버튼을 누를 경우 insert 문을 수행하는 함수 수행
        self.main_window.create_button = QPushButton("등록")
        self.main_window.create_button.clicked.connect(self.main_window.controller.input_data)
        create_h_layout4.addStretch(3)
        create_h_layout4.addWidget(self.main_window.create_button)
        create_h_layout4.addStretch(3)

        create_layout = QVBoxLayout()
        create_layout.addLayout(create_h_layout1)
        create_layout.addLayout(create_h_layout2)
        create_layout.addLayout(create_h_layout3)
        create_layout.addStretch(3)
        create_layout.addLayout(create_h_layout4)
        self.main_window.create_dialog.setLayout(create_layout)

        self.main_window.create_dialog.show()

    # 고객 정보 수정 화면
    def client_info_modify_view(self, rows):
        self.main_window.modify_dialog = QDialog()
        self.main_window.modify_dialog.setFixedWidth(320)
        self.main_window.modify_dialog.setFixedHeight(240)
        self.main_window.modify_dialog.setWindowTitle("고객 정보 수정")
        self.main_window.modify_dialog.setWindowModality(Qt.ApplicationModal)

        # 라벨, 기존 값, 수정 원하는 값 형태로 배치
        modify_h_layout1 = QHBoxLayout()
        label1 = QLabel("이름")
        text_browser1 = QTextBrowser()
        text_browser1.setFixedWidth(150)
        text_browser1.setFixedHeight(30)
        text_browser1.setText(rows[0][1])
        self.main_window.modify_line_edit1 = QLineEdit()
        self.main_window.modify_line_edit1.setFixedHeight(30)
        modify_h_layout1.addWidget(label1)
        modify_h_layout1.addWidget(text_browser1)
        modify_h_layout1.addWidget(self.main_window.modify_line_edit1)

        # 위와 동일
        modify_h_layout2 = QHBoxLayout()
        label2 = QLabel("등급")
        text_browser2 = QTextBrowser()
        text_browser2.setFixedWidth(150)
        text_browser2.setFixedHeight(30)
        text_browser2.setText(rows[0][2])
        self.main_window.modify_line_edit2 = QLineEdit()
        self.main_window.modify_line_edit2.setFixedHeight(30)
        modify_h_layout2.addWidget(label2)
        modify_h_layout2.addWidget(text_browser2)
        modify_h_layout2.addWidget(self.main_window.modify_line_edit2)

        # 위와 동일
        modify_h_layout3 = QHBoxLayout()
        label3 = QLabel("번호")
        text_browser3 = QTextBrowser()
        text_browser3.setFixedWidth(150)
        text_browser3.setFixedHeight(30)
        text_browser3.setText(rows[0][3])
        self.main_window.modify_line_edit3 = QLineEdit()
        self.main_window.modify_line_edit3.setFixedHeight(30)
        modify_h_layout3.addWidget(label3)
        modify_h_layout3.addWidget(text_browser3)
        modify_h_layout3.addWidget(self.main_window.modify_line_edit3)

        # "수정" 버튼에 update 쿼리를 수행하는 함수 연결
        modify_h_layout4 = QHBoxLayout()
        self.main_window.modify_button = QPushButton("수정")
        self.main_window.modify_button.clicked.connect(partial(self.main_window.controller.modify_data, rows))
        modify_h_layout4.addStretch(3)
        modify_h_layout4.addWidget(self.main_window.modify_button)
        modify_h_layout4.addStretch(3)

        modify_layout = QVBoxLayout()
        modify_layout.addLayout(modify_h_layout1)
        modify_layout.addLayout(modify_h_layout2)
        modify_layout.addLayout(modify_h_layout3)
        modify_layout.addStretch(3)
        modify_layout.addLayout(modify_h_layout4)
        self.main_window.modify_dialog.setLayout(modify_layout)
        self.main_window.modify_dialog.show()