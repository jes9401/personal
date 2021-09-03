from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import *
import pymysql
import sys
import os


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.set_ui()

    def set_ui(self):
        self.setWindowTitle('MyApp')
        self.setFixedWidth(640)
        self.setFixedHeight(480)
#
        tab0 = QWidget()

        tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        self.table1 = QTableWidget()
        self.table1.setEditTriggers(QAbstractItemView.NoEditTriggers)
        hlabels = ["고객 이름", "구매 건수", "원가 총합", "구매금액 총합"]
        self.table1.setColumnCount(len(hlabels))
        self.table1.setHorizontalHeaderLabels(hlabels)
        self.table1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tab1_layout.addWidget(self.table1)
        tab1.setLayout(tab1_layout)
        tab1.actionEvent(self.all_info())

        tab2 = QWidget()
        self.line_edit = QLineEdit()
        search_button = QPushButton("검색")
        search_button.clicked.connect(self.search)
        self.table2 = QTableWidget()
        self.table2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        hlabels = ["고객 이름", "전화 번호",""]
        self.table2.setColumnCount(len(hlabels))
        self.table2.setHorizontalHeaderLabels(hlabels)
        self.table2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tab2_layout_h = QHBoxLayout()
        tab2_layout_h.addWidget(self.line_edit)
        tab2_layout_h.addWidget(search_button)
        tab2_layout = QVBoxLayout()
        tab2_layout.addLayout(tab2_layout_h)
        tab2_layout.addWidget(self.table2)
        tab2.setLayout(tab2_layout)

        tab3 = QWidget()

        tabs = QTabWidget()
        tabs.addTab(tab0, '홈')
        tabs.addTab(tab1, '총 목록')
        tabs.addTab(tab2, '검색')
        tabs.addTab(tab3, '고객 관리')

        vbox = QVBoxLayout()
        vbox.addWidget(tabs)
        self.setLayout(vbox)

    def all_info(self):
        conn = pymysql.connect(host='localhost', user='root', password='root', db='mydb', charset='utf8')
        curs = conn.cursor()
        sql = "select * from all_info"
        curs.execute(sql)
        rows = curs.fetchall()
        self.table1.setRowCount(len(rows))
        self.table1.setColumnCount(4)
        for i in range(len(rows)):
            for j in range(4):
                self.table1.setItem(i, j, QTableWidgetItem(str(rows[i][j])))
        conn.close()

    def search(self):
        string = self.line_edit.text()
        # self.text_browser1.setText("")
        if len(string) != 0:
            conn = pymysql.connect(host='localhost', user='root', password='root', db='mydb', charset='utf8')
            curs = conn.cursor()
            sql = """select name, phone from client where name like '%"""+str(string)+"""%' or phone like '%"""+str(string)+"""%';"""
            curs.execute(sql)
            rows = curs.fetchall()
            self.table2.setRowCount(len(rows))
            self.table2.setColumnCount(2)
            if rows:
                for i in range(len(rows)):
                    for j in range(2):
                        self.table2.setItem(i, j, QTableWidgetItem(str(rows[i][j])))
            conn.close()
        else:
            self.table2.clear()
            self.table2.setItem(0,0 ,QTableWidgetItem("검색 결과가 없습니다."))



    def management(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    exit(app.exec_())

