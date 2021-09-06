from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import pymysql
import sys
from functools import partial


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.set_ui()

    def set_ui(self):
        self.setWindowTitle('MyApp')
        self.setFixedWidth(640)
        self.setFixedHeight(480)

        # tab1 => 총 목록
        tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        self.table1 = QTableWidget()
        self.table1.setEditTriggers(QAbstractItemView.NoEditTriggers)
        hlabels = ["고객 이름", "구매 건수", "원가 총합", "구매금액 총합", "거래 내역"]
        setHeader(self.table1, hlabels)
        tab1_layout.addWidget(self.table1)
        tab1.setLayout(tab1_layout)
        tab1.actionEvent(self.all_info())

        # tab2 => 검색
        tab2 = QWidget()
        self.line_edit = QLineEdit()
        search_button = QPushButton("검색")
        search_button.clicked.connect(self.search)
        self.table2 = QTableWidget()
        self.table2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        hlabels = ["고객 이름", "전화 번호", "등급", "거래 내역"]
        setHeader(self.table2, hlabels)
        tab2_layout_h = QHBoxLayout()
        tab2_layout_h.addWidget(self.line_edit)
        tab2_layout_h.addWidget(search_button)
        tab2_layout = QVBoxLayout()
        tab2_layout.addLayout(tab2_layout_h)
        tab2_layout.addWidget(self.table2)
        tab2.setLayout(tab2_layout)

        # tab3 => 고객관리
        tab3 = QWidget()
        self.add_button = QPushButton("고객 등록")
        self.add_button.clicked.connect(self.client_info_create)
        self.table3 = QTableWidget()
        self.table3.setEditTriggers(QAbstractItemView.NoEditTriggers)
        hlabels = ["고객 이름", "수정", "삭제"]
        setHeader(self.table3, hlabels)
        tab3_layout_h = QHBoxLayout()
        tab3_layout_h.addStretch(5)
        tab3_layout_h.addWidget(self.add_button)
        tab3_layout = QVBoxLayout()
        tab3_layout.addLayout(tab3_layout_h)
        tab3_layout.addWidget(self.table3)
        tab3.setLayout(tab3_layout)
        tab3.actionEvent(self.management())

        # 3개의 하위 탭을 TabWidget에 결합
        tabs = QTabWidget()
        tabs.addTab(tab1, '총 목록')
        tabs.addTab(tab2, '검색')
        tabs.addTab(tab3, '고객 관리')

        vbox = QVBoxLayout()
        vbox.addWidget(tabs)
        self.setLayout(vbox)

    # 총 목록 화면을 구성하는 함수
    def all_info(self):
        # 이름, 총 거래 건수, 원가 합, 구매 금액 총합을 조회하는 view
        # select a.name as "이름", IFNULL(b.cnt, 0) as "거래수",
        # IFNULL(b.p,0) as "원가합", IFNULL(b.bp,0) as "구매금액합"
        # from client as a left outer join(
        # 	select client_id, count(*) as cnt, sum(price) as p, sum(buy_price) as bp
        # 	from purchase
        # 	group by client_id
        # ) as b on a.client_id = b.client_id
        # order by b.p desc;
        sql = "select * from all_info;"
        rows = getQuery(sql)
        self.table1.setRowCount(len(rows))
        info_button_list = []
        for i in range(len(rows)):
            for j in range(4):
                self.table1.setItem(i, j, QTableWidgetItem(str(rows[i][j])))
            # 각 row별 버튼마다 클릭 이벤트 생성(매개변수 => 고객 이름)
            info_button = QPushButton("자세히")
            info_button_list.append(info_button)
            info_button_list[i].clicked.connect(partial(self.client_detail, rows[i][0]))
            self.table1.setCellWidget(i, 4, info_button_list[i])
    
    # 검색 화면 구성하는 함수
    def search(self):
        # 검색어 추출
        string = self.line_edit.text()
        
        # 검색창에 입력한 텍스트가 1자 이상일 경우에만 실행
        if len(string) != 0:
            # create view search_view as select name, phone, grade from client;
            sql = "select * from search_view where name like '%{}%' or phone like '%{}%';".format(str(string), str(string))
            rows = getQuery(sql)
            self.table2.setRowCount(len(rows))
            self.button_list = []
            # 조회 결과가 1개 이상일 경우
            if len(rows) > 0:
                for i in range(len(rows)):
                    for j in range(3):
                        self.table2.setItem(i, j, QTableWidgetItem(str(rows[i][j])))
                    button = QPushButton("자세히")
                    self.button_list.append(button)
                    # 고객 상세 화면으로 연결
                    self.button_list[i].clicked.connect(partial(self.client_detail, rows[i][0]))
                    self.table2.setCellWidget(i, 3, self.button_list[i])
            # 조회 결과가 없을 경우
            else:
                msg = msgBox("검색 결과가 없습니다.")
                msg.exec_()
        # 검색창에 아무것도 입력하지 않았을 경우
        else:
            self.table2.setRowCount(0)
            msg = msgBox("검색어를 입력하세요.")
            msg.exec_()

    # 고객 상세 화면
    def client_detail(self, client):
        # 등급에 따른 할인율
        grade = {"A": "20%", "B": "15%", "C": "10%", "D": "5%", "E": "0%"}
        
        # Dialog를 이용해 새 창 띄우기
        self.dialog = QDialog()
        self.dialog.setFixedWidth(640)
        self.dialog.setFixedHeight(360)
        self.dialog.setWindowTitle("{}님의 거래내역".format(client))
        # Qt.ApplicationModal => 다이얼로그를 실행시킨 부모 프로그램만 제어를 막는다.
        self.dialog.setWindowModality(Qt.ApplicationModal)

        client_detail_layout = QHBoxLayout()
        self.purchase_create_button = QPushButton("거래 내역 추가")
        # 거래내역 추가 화면으로 연결
        self.purchase_create_button.clicked.connect(partial(self.purchase_info_create, client))
        client_detail_layout.addStretch(5)
        client_detail_layout.addWidget(self.purchase_create_button)

        # 거래 내역이 들어갈 테이블 (상품명, 원가, 할인율, 구매금액, 삭제버튼)
        self.client_table = QTableWidget()
        # 해당 고객의 전체 거래 데이터 (총 거래 수, 원가 합, 구매금액의 합)
        self.client_table2 = QTableWidget()
        # NoEditTriggers => edit 금지 모드
        self.client_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.client_table2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        hlabels = ["상품명", "원가", "할인율", "구매 금액", "삭제"]
        hlabels2 = ["총 거래 수", "원가 합", " 총 구매금액"]
        # table 헤더 설정
        setHeader(self.client_table, hlabels)
        setHeader(self.client_table2, hlabels2)

        # 고객의 거래내역 조회를 위한 쿼리 (상품명, 원가, 등급, 구매 가격)
        # create view purchase_client_view as select a.name, b.product_name, b.price, a.grade, b.buy_price, b.date from client as a, purchase as b where a.client_id=b.client_id;
        sql = "select product_name, price, grade, buy_price from purchase_client_view where name = '{}' order by date desc;".format(client)

        rows = getQuery(sql)
        self.client_table.setRowCount(len(rows))
        purchase_delete_button_list = []
        for i in range(len(rows)):
            for j in range(4):
                # 할인율은 위에서 선언한 딕셔너리에 대입해서 value값 사용
                if j == 2:
                    self.client_table.setItem(i, j, QTableWidgetItem(grade[rows[i][j]]))
                else:
                    self.client_table.setItem(i, j, QTableWidgetItem(str(rows[i][j])))
            # 삭제 버튼 생성 및 거래 정보 삭제 함수와 연결
            purchase_delete_button = QPushButton("삭제")
            purchase_delete_button_list.append(purchase_delete_button)
            purchase_delete_button_list[i].clicked.connect(partial(self.purchase_info_delete, [client, rows[i][0], rows[i][1], rows[i][3]]))
            self.client_table.setCellWidget(i, 4, purchase_delete_button_list[i])

        # 고객의 전체 거래 데이터 (총 거래 수, 원가 합, 구매금액 합)
        sql = "select 거래수, 원가합, 구매금액합 from all_info where 이름 ='{}';".format(client)
        # sql = "select count(*), sum(b.price), sum(b.buy_price) from client as a, purchase as b where a.client_id=b.client_id group by a.name having a.name ='{}';".format(client)
        rows = getQuery(sql)
        self.client_table2.setRowCount(len(rows))
        for i in range(len(rows)):
            for j in range(3):
                self.client_table2.setItem(i, j, QTableWidgetItem(str(rows[i][j])))

        detail_layout = QVBoxLayout()
        detail_layout.addLayout(client_detail_layout)
        detail_layout.addWidget(self.client_table)
        detail_layout.addWidget(self.client_table2)
        self.dialog.setLayout(detail_layout)
        self.dialog.show()

    # 고객 정보 관리
    def management(self):
        # 고객의 이름만 조회
        sql = "select name from client;"
        rows = getQuery(sql)
        self.table3.setRowCount(len(rows))
        # 수정, 삭제 버튼을 저장할 리스트
        self.modify_button_list = []
        self.delete_button_list = []
        for i in range(len(rows)):
            self.table3.setItem(i, 0, QTableWidgetItem(str(rows[i][0])))
            modify_button = QPushButton("수정")
            delete_button = QPushButton("삭제")
            self.modify_button_list.append(modify_button)
            self.delete_button_list.append(delete_button)
            # 수정 기능, 삭제 기능을 진행하는 함수에 연결
            self.modify_button_list[i].clicked.connect(partial(self.client_info_modify, rows[i][0]))
            self.delete_button_list[i].clicked.connect(partial(self.client_info_delete, rows[i][0]))
            self.table3.setCellWidget(i, 1, self.modify_button_list[i])
            self.table3.setCellWidget(i, 2, self.delete_button_list[i])

    # 고객 정보 생성
    def client_info_create(self):
        self.create_dialog = QDialog()
        self.create_dialog.setFixedWidth(320)
        self.create_dialog.setFixedHeight(240)
        self.create_dialog.setWindowTitle("고객 등록")
        self.create_dialog.setWindowModality(Qt.ApplicationModal)

        create_h_layout1 = QHBoxLayout()
        label1 = QLabel("이름")
        self.create_line_edit1 = QLineEdit()
        create_h_layout1.addWidget(label1)
        create_h_layout1.addWidget(self.create_line_edit1)

        create_h_layout2 = QHBoxLayout()
        label2 = QLabel("등급")
        self.create_line_edit2 = QLineEdit()
        create_h_layout2.addWidget(label2)
        create_h_layout2.addWidget(self.create_line_edit2)

        create_h_layout3 = QHBoxLayout()
        label3 = QLabel("번호")
        self.create_line_edit3 = QLineEdit()
        create_h_layout3.addWidget(label3)
        create_h_layout3.addWidget(self.create_line_edit3)

        create_h_layout4 = QHBoxLayout()
        # "등록" 버튼을 누를 경우 insert 문을 수행하는 함수 수행
        self.create_button = QPushButton("등록")
        self.create_button.clicked.connect(self.input_data)
        create_h_layout4.addStretch(3)
        create_h_layout4.addWidget(self.create_button)
        create_h_layout4.addStretch(3)

        create_layout = QVBoxLayout()
        create_layout.addLayout(create_h_layout1)
        create_layout.addLayout(create_h_layout2)
        create_layout.addLayout(create_h_layout3)
        create_layout.addStretch(3)
        create_layout.addLayout(create_h_layout4)
        self.create_dialog.setLayout(create_layout)

        self.create_dialog.show()

    # 고객 정보 insert
    def input_data(self):
        name = self.create_line_edit1.text()
        grade = self.create_line_edit2.text()
        phone = self.create_line_edit3.text()
        # 세 칸 모두 입력한 값이 있으면 수행
        if len(name) != 0 and len(grade) != 0 and len(phone) != 0:
            sql = "insert into client(name,grade,phone) values('{}', '{}', '{}');".format(name, grade, phone)
            rows = getQuery(sql)
            msg = msgBox("등록 완료")
            msg.exec_()
            self.management()
            self.all_info()
            self.create_dialog.close()
        # 없을 경우 메시지 박스 출력
        else:
            msg = msgBox("모든 항목을 입력해주세요")
            msg.exec_()

    # 고객 정보 수정
    def client_info_modify(self, client):
        self.modify_dialog = QDialog()
        self.modify_dialog.setFixedWidth(320)
        self.modify_dialog.setFixedHeight(240)
        self.modify_dialog.setWindowTitle("고객 정보 수정")
        self.modify_dialog.setWindowModality(Qt.ApplicationModal)

        # 해당 고객의 정보를 조회(이름, 등급, 번호)
        sql = "select * from client where name = '{}';".format(client)
        rows = getQuery(sql)

        # 라벨, 기존 값, 수정 원하는 값 형태로 배치
        modify_h_layout1 = QHBoxLayout()
        label1 = QLabel("이름")
        text_browser1 = QTextBrowser()
        text_browser1.setFixedWidth(150)
        text_browser1.setFixedHeight(30)
        text_browser1.setText(rows[0][1])
        self.modify_line_edit1 = QLineEdit()
        self.modify_line_edit1.setFixedHeight(30)
        modify_h_layout1.addWidget(label1)
        modify_h_layout1.addWidget(text_browser1)
        modify_h_layout1.addWidget(self.modify_line_edit1)
        
        # 위와 동일
        modify_h_layout2 = QHBoxLayout()
        label2 = QLabel("등급")
        text_browser2 = QTextBrowser()
        text_browser2.setFixedWidth(150)
        text_browser2.setFixedHeight(30)
        text_browser2.setText(rows[0][2])
        self.modify_line_edit2 = QLineEdit()
        self.modify_line_edit2.setFixedHeight(30)
        modify_h_layout2.addWidget(label2)
        modify_h_layout2.addWidget(text_browser2)
        modify_h_layout2.addWidget(self.modify_line_edit2)
        
        # 위와 동일
        modify_h_layout3 = QHBoxLayout()
        label3 = QLabel("번호")
        text_browser3 = QTextBrowser()
        text_browser3.setFixedWidth(150)
        text_browser3.setFixedHeight(30)
        text_browser3.setText(rows[0][3])
        self.modify_line_edit3 = QLineEdit()
        self.modify_line_edit3.setFixedHeight(30)
        modify_h_layout3.addWidget(label3)
        modify_h_layout3.addWidget(text_browser3)
        modify_h_layout3.addWidget(self.modify_line_edit3)

        # "수정" 버튼에 update 쿼리를 수행하는 함수 연결
        modify_h_layout4 = QHBoxLayout()
        self.modify_button = QPushButton("수정")
        self.modify_button.clicked.connect(partial(self.modify_data, rows))
        modify_h_layout4.addStretch(3)
        modify_h_layout4.addWidget(self.modify_button)
        modify_h_layout4.addStretch(3)

        modify_layout = QVBoxLayout()
        modify_layout.addLayout(modify_h_layout1)
        modify_layout.addLayout(modify_h_layout2)
        modify_layout.addLayout(modify_h_layout3)
        modify_layout.addStretch(3)
        modify_layout.addLayout(modify_h_layout4)
        self.modify_dialog.setLayout(modify_layout)
        self.modify_dialog.show()

    def modify_data(self, rows):
        # update문 조건에 사용할 기존 이름
        past_name = rows[0][1]
        # lineedit에 작성된 텍스트 값들을 저장
        name = self.modify_line_edit1.text()
        grade = self.modify_line_edit2.text()
        phone = self.modify_line_edit3.text()
        # 3개의 칸에 하나도 입력한 내용이 없을 경우
        if len(name) == 0 and len(grade) == 0 and len(phone) == 0:
            msg = msgBox("변경 내용이 없습니다.")
            msg.exec_()
        # 있는 경우
        else:
            # 입력한 데이터가 없는 경우 기존 데이터로 대체, 있으면 새로 입력받은 값으로 대체
            name = rows[0][1] if len(name) == 0 else name
            grade = rows[0][2] if len(grade) == 0 else grade
            phone = rows[0][3] if len(phone) == 0 else phone
            sql = "update client set name='{}', grade='{}', phone='{}' where name = '{}';".format(name, grade, phone, past_name)
            rows = getQuery(sql)
        msg = msgBox("수정 완료")
        msg.exec_()
        self.management()
        self.all_info()
        self.modify_dialog.close()

    # 고객 정보 삭제
    def client_info_delete(self, client):
        reply = QMessageBox.question(self,' ', '정말 삭제하시겠습니까?', QMessageBox.Yes | QMessageBox.No)
        # Yes 버튼을 눌렀을 경우 해당 고객의 정보 삭제
        if reply == QMessageBox.Yes:
            sql = "delete from client where name = '{}';".format(client)
            rows = getQuery(sql)
            self.management()
            self.all_info()

    # 거래 정보 생성
    def purchase_info_create(self, client):
        self.purchase_create_dialog = QDialog()
        self.purchase_create_dialog.setFixedWidth(320)
        self.purchase_create_dialog.setFixedHeight(240)
        self.purchase_create_dialog.setWindowTitle("거래 등록")
        self.purchase_create_dialog.setWindowModality(Qt.ApplicationModal)
        
        purchase_create_h_layout1 = QHBoxLayout()
        label1 = QLabel("상품명")
        self.purchase_create_line_edit1 = QLineEdit()
        self.purchase_create_line_edit1.setFixedWidth(250)
        purchase_create_h_layout1.addWidget(label1)
        purchase_create_h_layout1.addWidget(self.purchase_create_line_edit1)

        purchase_create_h_layout2 = QHBoxLayout()
        label2 = QLabel("원가")
        self.purchase_create_line_edit2 = QLineEdit()
        self.purchase_create_line_edit2.setFixedWidth(250)
        purchase_create_h_layout2.addWidget(label2)
        purchase_create_h_layout2.addWidget(self.purchase_create_line_edit2)

        purchase_create_h_layout3 = QHBoxLayout()
        # "등록" 버튼 누를 경우 insert문 수행하는 함수 호출
        self.purchase_input_button = QPushButton("등록")
        self.purchase_input_button.clicked.connect(partial(self.input_purchase_data, client))
        purchase_create_h_layout3.addStretch(3)
        purchase_create_h_layout3.addWidget(self.purchase_input_button)
        purchase_create_h_layout3.addStretch(3)

        purchase_create_layout = QVBoxLayout()
        purchase_create_layout.addLayout(purchase_create_h_layout1)
        purchase_create_layout.addLayout(purchase_create_h_layout2)
        purchase_create_layout.addStretch(3)
        purchase_create_layout.addLayout(purchase_create_h_layout3)
        self.purchase_create_dialog.setLayout(purchase_create_layout)

        self.purchase_create_dialog.show()
    
    # 입력받은 데이터 insert하는 함수
    def input_purchase_data(self, client):
        # 할인율 적용을 위한 딕셔너리
        grade_dict = {"A": 0.8, "B": 0.85, "C": 0.9, "D": 0.95, "E": 1}
        product_name = self.purchase_create_line_edit1.text()
        price = self.purchase_create_line_edit2.text()
        # 상품명, 원가 둘다 입력 받은 경우에만 수행
        if len(product_name) !=0 and len(price) != 0:
            # 고객의 등급 조회 (A,B,C,D,E) 및 변수에 저장
            grade_sql = "select grade from client where name ='{}'".format(client)
            grade = getQuery(grade_sql)[0][0]
            # 고객 아이디, 상품명, 원가, 구매금액 row 생성
            sql = "insert into purchase(client_id, product_name, price, buy_price) values ((select client_id from client where name = '{}'), '{}', {}, {});".format(client, product_name, price, int(float(price)*grade_dict[grade]))
            rows = getQuery(sql)
            msg = msgBox("등록 완료")
            msg.exec_()
            self.management()
            self.all_info()
            self.purchase_create_dialog.close()
            self.client_detail(client)
        else:
            msg = msgBox("모든 항목을 입력해주세요")
            msg.exec_()

    # 거래 정보 삭제
    def purchase_info_delete(self, data):
        msg = msgBox("정말 삭제하시겠습니까?")
        msg.setStandardButtons((QMessageBox.Yes | QMessageBox.No))
        result = msg.exec_()
        if result == QMessageBox.Yes:
            # 고객 아이디, 상품명, 가격, 원가 4개 다 일치할 경우에 삭제
            sql = "delete from purchase where client_id = (select client_id from client where name ='{}') && product_name = '{}' && price = {} && buy_price = {};".format(data[0], data[1], data[2], data[3])
            rows = getQuery(sql)
            self.management()
            self.all_info()
            self.client_detail(data[0])


# 메시지박스 생성 함수
def msgBox(text):
    msg = QMessageBox()
    msg.setWindowTitle(" ")
    msg.setText(text)
    msg.setStandardButtons(QMessageBox.Yes)
    return msg


# sql 쿼리 수행하는 함수
def getQuery(sql):
    conn = pymysql.connect(host='localhost', user='root', password='root', db='mydb', charset='utf8')
    curs = conn.cursor()
    curs.execute(sql)
    data = curs.fetchall()
    conn.commit()
    conn.close()
    return data


# table 헤더 설정하는 함수
def setHeader(table, hlabels):
    table.setColumnCount(len(hlabels))
    table.setHorizontalHeaderLabels(hlabels)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    exit(app.exec_())

