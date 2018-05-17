# -*- coding: utf8 -*-

import pypyodbc
import xlrd
import datetime as dt
import sqlite3

# def sql(query,var=''):
#     # connection = pypyodbc.connect('Driver={SQL Server};Server=10.62.24.161\SQLEXPRESS;Database=web_cong_viec_amc;uid=aos;pwd=aos159753')
#     # connection = pypyodbc.connect('Driver={SQL Server};Server=10.62.24.161\SQLEXPRESS;Database=AMC_B;uid=aos;pwd=aos159753')
#     # connection = pypyodbc.connect('Driver={SQL Server};Server=10.62.24.161\SQLEXPRESS;Database=web_cong_viec_amc;uid=aos;pwd=aos159753')
#     connection = pypyodbc.connect('Driver={SQL Server};Server=10.62.24.161\SQLEXPRESS;Database=WEB_CONG_VIEC;uid=aos;pwd=aos159753')
#     # connection = pypyodbc.connect('Driver={SQL Server};Server=10.62.24.123,1433\SQL2008;Database=web_cong_viec_amc_mien_nam;uid=phunq;pwd=aos159753')

#     cursor = connection.cursor()
#     cursor.execute(query,var)
#     if query.lower()[:6] == 'select':
#         x = cursor.fetchall()
#         cursor.close()
#         return x
#     else:
#         cursor.commit()
#         cursor.close()

def sqlite(query,var=''):
    connection = sqlite3.connect(r'sm_tool.db')
    cursor = connection.cursor()
    cursor.execute(query,var)
    if query.lower()[:6] == 'select':
        x = cursor.fetchall()
        connection.close()
        return x
    elif query.lower()[:6] == 'create':
        connection.close()
    else:
        connection.commit()
        connection.close()



def str_to_dt(x):
    try:
        return dt.datetime.strptime(x,'%H:%M %d/%m/%Y')
    except:
        return dt.datetime.strptime(x,'%d/%m/%Y')

# n = xlrd.open_workbook(r'tho_cu_mb.xlsx')
# sheet = n.sheet_by_index(0)
# print (sheet.nrows)
# for i in range(1,sheet.nrows):
#     print(i)
#     name1 = sheet.cell(i,0).value
#     name2 = sheet.cell(i,1).value
#     name3 = sheet.cell(i,2).value
#     name4 = sheet.cell(i,3).value
#     name5 = sheet.cell(i,4).value
#     name6 = sheet.cell(i,5).value
#     name7 = sheet.cell(i,6).value
#     name8 = ''
#     name9 = name4 + ', ' + name3  + ', '+ name2  + ', '+ name1
#     name10 = 'MB'


#     # name9 = i
#     r = [name1, name2, name3, name4, name5, name6, name7, name8, name9, name10]
#     print(r)
#     sqlite("INSERT INTO data_mb values({})".format(",".join(["?"]*10)), r)



n = xlrd.open_workbook(r'quy_hoach.xlsx')
sheet = n.sheet_by_index(0)
print (sheet.nrows)

for i in range(1,sheet.nrows):
    print (i)
    name1 = sheet.cell(i,0).value
    name2 = sheet.cell(i,1).value
    name3 = sheet.cell(i,2).value
    name4 = sheet.cell(i,3).value
    name5 = sheet.cell(i,4).value
    name6 = sheet.cell(i,5).value
    name7 = sheet.cell(i,6).value
    name8 = sheet.cell(i,7).value
    name9 = sheet.cell(i,8).value

    r = [name1, name2, name3, name4, name5, name6, name7, name8, name9]

    sqlite("INSERT INTO thong_tin_quy_hoach values({})".format(",".join(["?"]*9)), r)



