import pyodbc
import time
import sys
from datetime import datetime
from socket import AF_INET, SOCK_DGRAM, SOCK_STREAM, socket, timeout
from struct import pack, unpack
import codecs
import cx_Oracle
import time

#con_ora = cx_Oracle.connect('lpg/lpg123@192.168.188.22/devdb')
#cur_ora = con_oracle.cursor()
#print(con_ora)

server = '192.168.12.70'
database = 'BioStar2_AC'
username = 'sa'
password = 'bat1#123'

con_sql = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'Trusted_Connection=yes;'
    f'UID={username};'
    f'PWD={password}'
)

cur_sql = conn.cursor()

query = "select * from dbo.T_CRD"
cur_sql.execute(query)
rows = cur_sql.fetchall()

for row in rows:
    print(row)

cur_sql.close()
con_sql.close()


while True:
    try:
        no_of_att_record = len(attendance_list)
        print(no_of_att_record)
        #print('Machine ' + str(attendance_list))
        for tpl in attendance_list:
            l_user_id = getattr(tpl,'user_id')
            l_attendance_date = getattr(tpl, 'timestamp')
            l_attendance_status = '01'
            l_punch_type = getattr(tpl, 'punch')
            l_unit_no = 9
            t_time = datetime.now()
            t_hour = t_time.hour
            print(t_hour)
            if l_user_id != '':
                cur_ora.callproc("push_attendance_date", [l_attendance_date,l_user_id,l_attendance_status,l_unit_no])
                con_ora.commit()
                print(l_user_id)
                print(l_attendance_date)
                print(tpl)
                time.sleep(.5)
                #if no_of_att_record > 1000 and ( t_hour >= 3 and t_hour < 4 ):
                    #conn.clear_attendance()
    except Exception as e:
        try:
            conn = zk.connect()
            con_oracle = cx_Oracle.connect('lpg/lpg123@192.168.188.22/devdb')
            cur_oracle = con_oracle.cursor()
            print('Exception' + str(conn))
            print('Exception ' + str(e))
        except:
            pass
