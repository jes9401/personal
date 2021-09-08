from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from functools import partial


class Tab1View():
    def __init__(self, main_window):
        self.main_window = main_window

    # 1번째 탭 구현(총 목록)
    def tab1(self):
        tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        self.main_window.table1 = QTableWidget()
        self.main_window.table1.setEditTriggers(QAbstractItemView.NoEditTriggers)
        hlabels = ["고객 이름", "구매 건수", "원가 총합", "구매금액 총합", "거래 내역"]
        self.main_window.model.set_header(self.main_window.table1, hlabels)
        tab1_layout.addWidget(self.main_window.table1)
        tab1.setLayout(tab1_layout)
        tab1.actionEvent(self.main_window.controller.all_info())
        return tab1

    # 총 목록 화면
    def tab1_reload(self, rows):
        self.main_window.table1.setRowCount(len(rows))
        info_button_list = []
        for i in range(len(rows)):
            for j in range(4):
                self.main_window.table1.setItem(i, j, QTableWidgetItem(str(rows[i][j])))
            # 각 row별 버튼마다 클릭 이벤트 생성(매개변수 => 고객 이름)
            info_button = QPushButton("자세히")
            info_button_list.append(info_button)
            info_button_list[i].clicked.connect(partial(self.main_window.controller.client_detail, rows[i][0]))
            self.main_window.table1.setCellWidget(i, 4, info_button_list[i])

    # 고객의 거래 내역 화면(자세히 버튼 눌렀을 때)
    def client_detail_view(self, rows1, rows2, client):
        # Dialog를 이용해 새 창 띄우기
        self.main_window.dialog = QDialog()
        self.main_window.dialog.setFixedWidth(640)
        self.main_window.dialog.setFixedHeight(360)
        self.main_window.dialog.setWindowTitle("{}님의 거래내역".format(client))
        # Qt.ApplicationModal => 다이얼로그를 실행시킨 부모 프로그램만 제어를 막는다.
        self.main_window.dialog.setWindowModality(Qt.ApplicationModal)

        client_detail_layout = QHBoxLayout()
        self.main_window.purchase_create_button = QPushButton("거래 내역 추가")
        # 거래내역 추가 화면으로 연결
        self.main_window.purchase_create_button.clicked.connect(partial(self.main_window.controller.purchase_create, client))
        client_detail_layout.addStretch(5)
        client_detail_layout.addWidget(self.main_window.purchase_create_button)

        # 거래 내역이 들어갈 테이블 (상품명, 원가, 할인율, 구매금액, 삭제버튼)
        self.main_window.client_table = QTableWidget()
        # 해당 고객의 전체 거래 데이터 (총 거래 수, 원가 합, 구매금액의 합)
        self.main_window.client_table2 = QTableWidget()
        # NoEditTriggers => edit 금지 모드
        self.main_window.client_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.main_window.client_table2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        hlabels = ["상품명", "원가", "할인율", "구매 금액", "삭제"]
        hlabels2 = ["총 거래 수", "원가 합", " 총 구매금액"]
        # table 헤더 설정
        self.main_window.model.set_header(self.main_window.client_table, hlabels)
        self.main_window.model.set_header(self.main_window.client_table2, hlabels2)
        self.main_window.client_table.setRowCount(len(rows1))
        purchase_delete_button_list = []
        for i in range(len(rows1)):
            for j in range(4):
                if j == 2:
                    grade_sql = "select discount from grade_table where grade='{}'".format(rows1[i][2])
                    grade_rows = str(self.main_window.model.get_query(grade_sql)[0][0]) + "%"
                    self.main_window.client_table.setItem(i, j, QTableWidgetItem(grade_rows))
                else:
                    self.main_window.client_table.setItem(i, j, QTableWidgetItem(str(rows1[i][j])))
            # 삭제 버튼 생성 및 거래 정보 삭제 함수와 연결
            purchase_delete_button = QPushButton("삭제")
            purchase_delete_button_list.append(purchase_delete_button)
            purchase_delete_button_list[i].clicked.connect(
                partial(self.main_window.controller.purchase_info_delete, [client, rows1[i][0], rows1[i][1], rows1[i][3]]))
            self.main_window.client_table.setCellWidget(i, 4, purchase_delete_button_list[i])

        self.main_window.client_table2.setRowCount(len(rows2))
        for i in range(len(rows2)):
            for j in range(3):
                self.main_window.client_table2.setItem(i, j, QTableWidgetItem(str(rows2[i][j])))

        detail_layout = QVBoxLayout()
        detail_layout.addLayout(client_detail_layout)
        detail_layout.addWidget(self.main_window.client_table)
        detail_layout.addWidget(self.main_window.client_table2)
        self.main_window.dialog.setLayout(detail_layout)
        self.main_window.dialog.show()

    # 거래 정보 생성 창
    def purchase_create_view(self, client):
        self.main_window.purchase_create_dialog = QDialog()
        self.main_window.purchase_create_dialog.setFixedWidth(320)
        self.main_window.purchase_create_dialog.setFixedHeight(240)
        self.main_window.purchase_create_dialog.setWindowTitle("거래 등록")
        self.main_window.purchase_create_dialog.setWindowModality(Qt.ApplicationModal)

        purchase_create_h_layout1 = QHBoxLayout()
        label1 = QLabel("상품명")
        self.main_window.purchase_create_line_edit1 = QLineEdit()
        self.main_window.purchase_create_line_edit1.setFixedWidth(250)
        purchase_create_h_layout1.addWidget(label1)
        purchase_create_h_layout1.addWidget(self.main_window.purchase_create_line_edit1)

        purchase_create_h_layout2 = QHBoxLayout()
        label2 = QLabel("원가")
        self.main_window.purchase_create_line_edit2 = QLineEdit()
        self.main_window.purchase_create_line_edit2.setFixedWidth(250)
        purchase_create_h_layout2.addWidget(label2)
        purchase_create_h_layout2.addWidget(self.main_window.purchase_create_line_edit2)

        purchase_create_h_layout3 = QHBoxLayout()
        self.main_window.purchase_input_button = QPushButton("등록")
        self.main_window.purchase_input_button.clicked.connect(partial(self.main_window.controller.input_purchase_data, client))
        purchase_create_h_layout3.addStretch(3)
        purchase_create_h_layout3.addWidget(self.main_window.purchase_input_button)
        purchase_create_h_layout3.addStretch(3)

        purchase_create_layout = QVBoxLayout()
        purchase_create_layout.addLayout(purchase_create_h_layout1)
        purchase_create_layout.addLayout(purchase_create_h_layout2)
        purchase_create_layout.addStretch(3)
        purchase_create_layout.addLayout(purchase_create_h_layout3)
        self.main_window.purchase_create_dialog.setLayout(purchase_create_layout)
        self.main_window.purchase_create_dialog.show()
