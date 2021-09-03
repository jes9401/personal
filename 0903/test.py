import sys
from PyQt5.QtWidgets import *
import pymysql

string ="1"
conn = pymysql.connect(host='localhost', user='root', password='root', db='mydb', charset='utf8')
curs = conn.cursor()
sql = """select name, phone from client where name like '%"""+str(string)+"""%' or phone like '%"""+str(string)+"""%';"""
curs.execute(sql)
rows = curs.fetchall()
print(rows)