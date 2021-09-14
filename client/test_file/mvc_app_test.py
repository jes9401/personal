import sys
import os
import pymysql
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from functools import partial


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


class Model(QtCore.QObject):
    def __init__(self):
        super().__init__()

    # sql 쿼리 수행하는 함수
    def getQuery(self, sql):
        conn = pymysql.connect(host='localhost', user='root', password='root', db='mydb', charset='utf8')
        curs = conn.cursor()
        curs.execute(sql)
        data = curs.fetchall()
        conn.commit()
        conn.close()
        return data

    # table 헤더 설정하는 함수
    def setHeader(self, table, hlabels):
        table.setColumnCount(len(hlabels))
        table.setHorizontalHeaderLabels(hlabels)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def msgBox(self, text):
        msg = QMessageBox()
        msg.setWindowTitle(" ")
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Yes)
        return msg


class View1():
    def __init__(self, main_window):
        self.main_window = main_window

    def tab1(self):
        tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        self.main_window.table1 = QTableWidget()
        self.main_window.table1.setEditTriggers(QAbstractItemView.NoEditTriggers)
        hlabels = ["고객 이름", "구매 건수", "원가 총합", "구매금액 총합", "거래 내역"]
        self.main_window.model.setHeader(self.main_window.table1, hlabels)
        tab1_layout.addWidget(self.main_window.table1)
        tab1.setLayout(tab1_layout)
        tab1.actionEvent(self.main_window.controller.all_info())
        return tab1

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
        self.main_window.purchase_create_button.clicked.connect(partial(self.main_window.controller.purchase_info_create, client))
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
        self.main_window.model.setHeader(self.main_window.client_table, hlabels)
        self.main_window.model.setHeader(self.main_window.client_table2, hlabels2)
        self.main_window.client_table.setRowCount(len(rows1))
        purchase_delete_button_list = []
        for i in range(len(rows1)):
            for j in range(4):
                # 할인율은 위에서 선언한 딕셔너리에 대입해서 value값 사용
                if j == 2:
                    grade_sql = "select discount from grade_table where grade='{}'".format(rows1[i][2])
                    grade_rows = str(self.main_window.model.getQuery(grade_sql)[0][0]) + "%"
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


class View2():
    def __init__(self, main_window):
        self.main_window = main_window

    def tab2(self):
        # tab2 => 검색
        tab2 = QWidget()
        self.main_window.line_edit = QLineEdit()
        search_button = QPushButton("검색")
        search_button.clicked.connect(self.main_window.controller.search)
        self.main_window.table2 = QTableWidget()
        self.main_window.table2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        hlabels = ["고객 이름", "전화 번호", "등급", "거래 내역"]
        self.main_window.model.setHeader(self.main_window.table2, hlabels)
        tab2_layout_h = QHBoxLayout()
        tab2_layout_h.addWidget(self.main_window.line_edit)
        tab2_layout_h.addWidget(search_button)
        tab2_layout = QVBoxLayout()
        tab2_layout.addLayout(tab2_layout_h)
        tab2_layout.addWidget(self.main_window.table2)
        tab2.setLayout(tab2_layout)
        return tab2

    def search_view(self, rows):
        for i in range(len(rows)):
            for j in range(3):
                self.main_window.table2.setItem(i, j, QTableWidgetItem(str(rows[i][j])))
            button = QPushButton("자세히")
            self.main_window.button_list.append(button)
            # 고객 상세 화면으로 연결
            self.main_window.button_list[i].clicked.connect(partial(self.main_window.controller.client_detail, rows[i][0]))
            self.main_window.table2.setCellWidget(i, 3, self.main_window.button_list[i])


class View3():
    def __init__(self, main_window):
        self.main_window = main_window

    def tab3(self):
        # tab3 => 고객관리
        tab3 = QWidget()
        self.add_button = QPushButton("고객 등록")
        self.add_button.clicked.connect(self.main_window.view3.client_info_create_view)
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


class Controller():
    def __init__(self, main_window):
        self.main_window = main_window
    # 총 목록 화면을 구성하는 함수

    def all_info(self):
        sql = "select * from all_info;"
        rows = self.main_window.model.getQuery(sql)
        self.main_window.view1.tab1_reload(rows)

    def client_detail(self, client):
        # 고객의 거래내역 조회를 위한 쿼리 (상품명, 원가, 등급, 구매 가격)
        # create view purchase_client_view as select a.name, b.product_name, b.price, a.grade, b.buy_price, b.date from client as a, purchase as b where a.client_id=b.client_id;
        sql = "select product_name, price, grade, buy_price from purchase_client_view where name = '{}' order by date desc;".format(
            client)

        rows1 = self.main_window.model.getQuery(sql)

        # 고객의 전체 거래 데이터 (총 거래 수, 원가 합, 구매금액 합)
        sql = "select 거래수, 원가합, 구매금액합 from all_info where 이름 ='{}';".format(client)
        rows2 = self.main_window.model.getQuery(sql)
        self.main_window.view1.client_detail_view(rows1, rows2, client)

    def purchase_info_create(self, client):
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
        # "등록" 버튼 누를 경우 insert문 수행하는 함수 호출
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

    def input_purchase_data(self, client):
        product_name = self.main_window.purchase_create_line_edit1.text()
        price = self.main_window.purchase_create_line_edit2.text()
        # 상품명, 원가 둘다 입력 받은 경우에만 수행
        if len(product_name) != 0 and len(price) != 0:
            # 고객 아이디, 상품명, 원가, 구매금액 row 생성
            sql = "insert into purchase(client_id, product_name, price, buy_price) values((select client_id from client where name ='{}'), '{}', {}, {}-({}*(select discount from grade_table where grade = (select grade from client where name='{}')) div 100));".format(
                client, product_name, price, price, price, client)
            rows = self.main_window.model.getQuery(sql)
            msg = self.main_window.model.msgBox("등록 완료")
            msg.exec_()
            self.reload()
            self.main_window.purchase_create_dialog.close()
            self.client_detail(client)
        else:
            msg = self.main_window.model.msgBox("모든 항목을 입력해주세요")
            msg.exec_()

    # 거래 정보 삭제
    def purchase_info_delete(self, data):
        msg = self.main_window.model.msgBox("정말 삭제하시겠습니까?")
        msg.setStandardButtons((QMessageBox.Yes | QMessageBox.No))
        result = msg.exec_()
        if result == QMessageBox.Yes:
            # 고객 아이디, 상품명, 가격, 원가 4개 다 일치할 경우에 삭제
            sql = "delete from purchase where client_id = (select client_id from client where name ='{}') && product_name = '{}' && price = {} && buy_price = {};".format(
                data[0], data[1], data[2], data[3])
            rows = self.main_window.model.getQuery(sql)
            self.client_detail(data[0])
            self.reload()

    def search(self):
        # 검색어 추출
        string = self.main_window.line_edit.text()

        # 검색창에 입력한 텍스트가 1자 이상일 경우에만 실행
        if len(string) != 0:
            # create view search_view as select name, phone, grade from client;
            sql = "select * from search_view where name like '%{}%' or phone like '%{}%';".format(str(string),
                                                                                                  str(string))
            rows = self.main_window.model.getQuery(sql)
            self.main_window.table2.setRowCount(len(rows))
            self.main_window.button_list = []
            # 조회 결과가 1개 이상일 경우
            if len(rows) > 0:
                self.main_window.view2.search_view(rows)
            # 조회 결과가 없을 경우
            else:
                msg = self.main_window.model.msgBox("검색 결과가 없습니다.")
                msg.exec_()
        # 검색창에 아무것도 입력하지 않았을 경우
        else:
            self.main_window.table2.setRowCount(0)
            msg = self.main_window.model.msgBox("검색어를 입력하세요.")
            msg.exec_()

    def management(self):
        # 고객의 이름만 조회
        sql = "select name from client;"
        rows = self.main_window.model.getQuery(sql)
        self.main_window.view3.management_view(rows)

    # 고객 정보 insert
    def input_data(self):
        name = self.main_window.create_line_edit1.text()
        grade = self.main_window.create_line_edit2.text()
        phone = self.main_window.create_line_edit3.text()
        # 세 칸 모두 입력한 값이 있으면 수행
        if len(name) != 0 and len(grade) != 0 and len(phone) != 0:
            sql = "insert into client(name,grade,phone) values('{}', '{}', '{}');".format(name, grade, phone)
            rows = self.main_window.model.getQuery(sql)
            msg = self.main_window.model.msgBox("등록 완료")
            msg.exec_()
            self.main_window.create_dialog.close()
            self.reload()
        # 없을 경우 메시지 박스 출력
        else:
            msg = self.main_window.model.msgBox("모든 항목을 입력해주세요")
            msg.exec_()

    # 고객 정보 삭제
    def client_info_delete(self, client):
        reply = QMessageBox.question(self.main_window, ' ', '정말 삭제하시겠습니까?', QMessageBox.Yes | QMessageBox.No)
        # Yes 버튼을 눌렀을 경우 해당 고객의 정보 삭제
        if reply == QMessageBox.Yes:
            sql = "delete from client where name = '{}';".format(client)
            rows = self.main_window.model.getQuery(sql)
            self.reload()

    def client_info_modify(self, client):
        # 해당 고객의 정보를 조회(이름, 등급, 번호)
        sql = "select * from client where name = '{}';".format(client)
        rows = self.main_window.model.getQuery(sql)
        self.main_window.view3.client_info_modify_view(rows)

    def modify_data(self, rows):
        # update문 조건에 사용할 기존 이름
        past_name = rows[0][1]
        # lineedit에 작성된 텍스트 값들을 저장
        name = self.main_window.modify_line_edit1.text()
        grade = self.main_window.modify_line_edit2.text()
        phone = self.main_window.modify_line_edit3.text()
        # 3개의 칸에 하나도 입력한 내용이 없을 경우
        if len(name) == 0 and len(grade) == 0 and len(phone) == 0:
            msg = self.main_window.model.msgBox("변경 내용이 없습니다.")
            msg.exec_()
        # 있는 경우
        else:
            # 입력한 데이터가 없는 경우 기존 데이터로 대체, 있으면 새로 입력받은 값으로 대체
            name = rows[0][1] if len(name) == 0 else name
            grade = rows[0][2] if len(grade) == 0 else grade
            phone = rows[0][3] if len(phone) == 0 else phone
            sql = "update client set name='{}', grade='{}', phone='{}' where name = '{}';".format(name, grade, phone,
                                                                                                  past_name)
            rows = self.main_window.model.getQuery(sql)
        msg = self.main_window.model.msgBox("수정 완료")
        msg.exec_()
        self.reload()
        self.main_window.modify_dialog.close()

    def reload(self):
        self.all_info()
        self.management()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MainWindow()
    form.setWindowTitle('Haha..')
    form.setFixedWidth(640)
    form.setFixedHeight(480)
    form.show()
    exit(app.exec_())