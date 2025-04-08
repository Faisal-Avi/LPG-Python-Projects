import requests
import re
import cx_Oracle
import time
import base64
  
url = "https://gpcmp.grameenphone.com/gpcmpapi/messageplatform/controller.home?username=BeximcoLPG1&password=Admin123@&apicode=1&msisdn=#&countrycode=880&cli=~~&messagetype=1&message=***&messageid=0"

con = cx_Oracle.connect('u/p@ip/sid')
cur_oracle = con.cursor()

while True:
	print('.................')
	try:
		oracle_sql = '''SELECT sms_text,
							   masking_name,
							   receiver_no,
							   sms_outgoing_id
						FROM gbl_sms_outgoing
						WHERE sms_status = 'N' '''
		cur_oracle.execute(oracle_sql);

		l_list = cur_oracle.fetchall()
	
		for tpl in l_list:
			l_sms_text = tpl[0]
			l_masking_name = tpl[1]
			l_receiver_no = tpl[2]
			l_sms_outgoing_id = tpl[3]
			l_sms_text = l_sms_text.encode('utf-8')
		
			l_url = url.replace('#', l_receiver_no)
			l_url = l_url.replace('~~', l_masking_name)
			l_url = l_url.replace('***', l_sms_text)
		
			try:
				response = requests.get(l_url)
				cur_oracle.callproc("gbl_supp.upd_gbl_sms_outgoing", [l_sms_outgoing_id])
				con.commit()
				print(response)
				print('SMS Sent Successfully')
			except:
				print("Something went wrong")
	except Exception as e:
		try:
			con = cx_Oracle.connect('u/p@ip/sid')
			cur_oracle = con.cursor()		
		except Exception as e:
			pass
		
	time.sleep(1)
