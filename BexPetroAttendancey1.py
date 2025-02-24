#from zklib import zklib, zkconst
from zk import ZK, const
from zk import ZK, const
from zk.base import ZK_helper
from zk.user import User
from zk.finger import Finger
from zk.attendance import Attendance
from zk.exception import ZKErrorResponse, ZKNetworkError, ZKErrorConnection, ZKErrorResponse, ZKNetworkError
import time

import sys
from datetime import datetime
from socket import AF_INET, SOCK_DGRAM, SOCK_STREAM, socket, timeout
from struct import pack, unpack
import codecs
import cx_Oracle
import time

con = cx_Oracle.connect('lpg/lpg123@192.168.188.22/devdb')
cur_oracle = con.cursor()
zk = ZK('192.168.189.7', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
conn = zk.connect()
print(conn)

while True:
    try:
        attendance_list = conn.get_attendance()
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
                cur_oracle.callproc("push_attendance_date1", [l_attendance_date,l_user_id,l_attendance_status,l_unit_no])
                con.commit()
                print(l_user_id)
                print(l_attendance_date)
                print(tpl)
                time.sleep(.5)
                #if no_of_att_record > 1000 and ( t_hour >= 3 and t_hour < 4 ):
                    #conn.clear_attendance()
    except Exception as e:
        try:
            conn = zk.connect()
            con = cx_Oracle.connect('lpg/lpg123@192.168.188.22/devdb')
            cur_oracle = con.cursor()
            print('Exception' + str(conn))
            print('Exception ' + str(e))
        except:
            pass



