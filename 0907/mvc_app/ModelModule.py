import pymysql
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import mysql_auth


class Model(QtCore.QObject):
    def __init__(self):
        super().__init__()

    # sql 쿼리 수행하는 함수
    def getQuery(self, sql):
        mysql_info = mysql_auth.info
        conn = pymysql.connect(host=mysql_info['host'], user=mysql_info['user'], password=mysql_info['passwd'], db=mysql_info['db'], charset=mysql_info['charset'])
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

    # 메시지박스 생성
    def msgBox(self, text):
        msg = QMessageBox()
        msg.setWindowTitle(" ")
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Yes)
        return msg
