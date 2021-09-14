from PyQt5.QtWidgets import *


class Controller():
    def __init__(self, main_window):
        self.main_window = main_window

    # 총 목록 화면을 구성하는 함수
    def all_info(self):
        sql = "select * from all_info;"
        rows = self.main_window.model.get_query(sql)
        self.main_window.tab1_view.tab1_reload(rows)

    # 고객 상세 화면 (자세히 버튼 눌렀을 때)
    def client_detail(self, client):
        # 고객의 거래내역 조회를 위한 쿼리 (상품명, 원가, 등급, 구매 가격)
        sql = "select product_name, price, grade, buy_price from purchase_client_view where name = '{}' order by date desc;".format(
            client)

        rows1 = self.main_window.model.get_query(sql)

        # 고객의 전체 거래 데이터 (총 거래 수, 원가 합, 구매금액 합)
        sql = "select purchase_count, sum_price, sum_buyprice from all_info where name ='{}';".format(client)
        rows2 = self.main_window.model.get_query(sql)
        self.main_window.tab1_view.client_detail_view(rows1, rows2, client)
    
    # 거래 정보 생성 창
    def purchase_create(self, client):
        self.main_window.tab1_view.purchase_create_view(client)
    
    # 거래 정보 생성
    def input_purchase_data(self, client):
        product_name = self.main_window.purchase_create_line_edit1.text()
        price = self.main_window.purchase_create_line_edit2.text()
        # 상품명, 원가 둘다 입력 받은 경우에만 수행
        if len(product_name) != 0 and len(price) != 0:
            # 고객 아이디, 상품명, 원가, 구매금액 row 생성
            sql = "insert into purchase(client_id, product_name, price, buy_price) values((select client_id from client where name ='{}'), '{}', {}, {}-({}*(select discount from grade_table where grade = (select grade from client where name='{}')) div 100));".format(
                client, product_name, price, price, price, client)
            rows = self.main_window.model.get_query(sql)
            msg = self.main_window.model.create_msgbox("등록 완료")
            msg.exec_()
            self.reload()
            self.main_window.purchase_create_dialog.close()
            self.client_detail(client)
        else:
            msg = self.main_window.model.create_msgbox("모든 항목을 입력해주세요")
            msg.exec_()

    # 거래 정보 삭제
    def purchase_info_delete(self, data):
        msg = self.main_window.model.create_msgbox("정말 삭제하시겠습니까?")
        msg.setStandardButtons((QMessageBox.Yes | QMessageBox.No))
        result = msg.exec_()
        if result == QMessageBox.Yes:
            # 고객 아이디, 상품명, 가격, 원가 4개 다 일치할 경우에 삭제
            sql = "delete from purchase where client_id = (select client_id from client where name ='{}') && product_name = '{}' && price = {} && buy_price = {};".format(
                data[0], data[1], data[2], data[3])
            rows = self.main_window.model.get_query(sql)
            self.client_detail(data[0])
            self.reload()

    # 검색 화면
    def search(self):
        # 검색어 추출
        string = self.main_window.line_edit.text()

        # 검색창에 입력한 텍스트가 1자 이상일 경우에만 실행
        if len(string) != 0:
            # create view search_view as select name, phone, grade from client;
            sql = "select * from search_view where name like '%{}%' or phone like '%{}%';".format(str(string),
                                                                                                  str(string))
            rows = self.main_window.model.get_query(sql)
            self.main_window.table2.setRowCount(len(rows))
            self.main_window.button_list = []
            # 조회 결과가 1개 이상일 경우
            if len(rows) > 0:
                self.main_window.tab2_view.search_view(rows)
            # 조회 결과가 없을 경우
            else:
                msg = self.main_window.model.create_msgbox("검색 결과가 없습니다.")
                msg.exec_()
        # 검색창에 아무것도 입력하지 않았을 경우
        else:
            self.main_window.table2.setRowCount(0)
            msg = self.main_window.model.create_msgbox("검색어를 입력하세요.")
            msg.exec_()

    # 고객 관리
    def management(self):
        # 고객의 이름만 조회
        sql = "select name from client;"
        rows = self.main_window.model.get_query(sql)
        self.main_window.tab3_view.management_view(rows)

    # 고객 정보 insert
    def input_data(self):
        name = self.main_window.create_line_edit1.text()
        # grade = self.main_window.create_line_edit2.text()
        grade = self.main_window.create_combobox.currentText()
        phone = self.main_window.create_line_edit3.text()
        # 세 칸 모두 입력한 값이 있으면 수행
        if len(name) != 0 and len(grade) != 0 and len(phone) != 0:
            sql = "insert into client(name,grade,phone) values('{}', '{}', '{}');".format(name, grade, phone)
            rows = self.main_window.model.get_query(sql)
            msg = self.main_window.model.create_msgbox("등록 완료")
            msg.exec_()
            self.main_window.create_dialog.close()
            self.reload()
        # 없을 경우 메시지 박스 출력
        else:
            msg = self.main_window.model.create_msgbox("모든 항목을 입력해주세요")
            msg.exec_()

    # 고객 정보 삭제
    def client_info_delete(self, client):
        reply = QMessageBox.question(self.main_window, ' ', '정말 삭제하시겠습니까?', QMessageBox.Yes | QMessageBox.No)
        # Yes 버튼을 눌렀을 경우 해당 고객의 정보 삭제
        if reply == QMessageBox.Yes:
            sql = "delete from client where name = '{}';".format(client)
            rows = self.main_window.model.get_query(sql)
            self.reload()
    
    # 고객 정보 수정
    def client_info_modify(self, client):
        # 해당 고객의 정보를 조회(이름, 등급, 번호)
        sql = "select * from client where name = '{}';".format(client)
        rows = self.main_window.model.get_query(sql)
        self.main_window.tab3_view.client_info_modify_view(rows)
    
    # 고객 정보 수정
    def modify_data(self, rows):
        # update문 조건에 사용할 기존 이름
        past_name = rows[0][1]
        # lineedit에 작성된 텍스트 값들을 저장
        name = self.main_window.modify_line_edit1.text()
        grade = self.main_window.modify_line_edit2.text()
        phone = self.main_window.modify_line_edit3.text()
        # 3개의 칸에 하나도 입력한 내용이 없을 경우
        if len(name) == 0 and len(grade) == 0 and len(phone) == 0:
            msg = self.main_window.model.create_msgbox("변경 내용이 없습니다.")
            msg.exec_()
        # 있는 경우
        else:
            # 입력한 데이터가 없는 경우 기존 데이터로 대체, 있으면 새로 입력받은 값으로 대체
            name = rows[0][1] if len(name) == 0 else name
            grade = rows[0][2] if len(grade) == 0 else grade
            phone = rows[0][3] if len(phone) == 0 else phone
            sql = "update client set name='{}', grade='{}', phone='{}' where name = '{}';".format(name, grade, phone,
                                                                                                  past_name)
            rows = self.main_window.model.get_query(sql)
            msg = self.main_window.model.create_msgbox("수정 완료")
            msg.exec_()
            self.reload()
            self.main_window.modify_dialog.close()
    
    # 화면 동기화(총 목록, 고객 관리)
    def reload(self):
        self.all_info()
        self.management()
