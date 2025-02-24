import requests
import re
import cx_Oracle
import time
import qrcode
from io import BytesIO
from pypdf import PdfReader, PdfWriter

con = cx_Oracle.connect('lpg_bkp/lpg123456@192.168.188.32/dbtest')
cur_oracle = con.cursor()

while True:
	#print('.................')
	try:
		oracle_sql = '''SELECT string,
                               id
						FROM gbl_qrcode_generate
						WHERE is_generated = 'N' '''
		cur_oracle.execute(oracle_sql);

		l_list = cur_oracle.fetchall()
	
		for tpl in l_list:
			l_string = tpl[0]
			l_id = tpl[1]       
			try:
				buffer = BytesIO()
				qr = qrcode.QRCode(version=1, box_size=10, border=5)
				data = l_string
				qr.add_data(data)
				qr.make(fit=True)
				img = qr.make_image(fill_color="black", back_color="white")
                img2 = qr.make(fill_color="black", back_color="white")
                img2.save("qrcode.pdf")
				img.save(buffer)
				blob_data = buffer.getvalue()
				img.save("qrcode.jpg")
				#print(img)
				cur_oracle.callproc("gbl_supp.upd_qrcode_generate", [l_id,blob_data])
				con.commit()
				print('Updated Successfully')
			except Exception as e:
				print(e)
	except Exception as e:
		try:
			con = cx_Oracle.connect('lpg_bkp/lpg123456@192.168.188.32/dbtest')
			cur_oracle = con.cursor()		
		except Exception as e:
			pass
		
	time.sleep(1)