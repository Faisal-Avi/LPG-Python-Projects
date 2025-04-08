from geopy.geocoders import Nominatim
from geopy.geocoders import Photon
import geocoder
import cx_Oracle
import time

con = cx_Oracle.connect('u/p@ip/sid')
cur_oracle = con.cursor()

while True:
	try:
		oracle_sql = '''SELECT latitude, 
							   longitude,
							   attendance_id
						FROM attendance_activity
						WHERE ( attendance_loc LIKE '%html%'
								OR attendance_loc LIKE '%not found%') '''
		cur_oracle.execute(oracle_sql)
		l_list = cur_oracle.fetchall()
		print(l_list)
		for tpl in l_list:
			try:
				k_latitude = tpl[0]
				k_longitude = tpl[1]
				k_attendance_id = tpl[2]
				l_longitude = k_longitude
				l_latitude = k_latitude
				Latitude = l_latitude
				Longitude = l_longitude
				coordinates = f"{Latitude}, {Longitude}"
				geolocator = Photon(user_agent="measurements")
				location = geolocator.reverse(coordinates, language="en")
				l_location = location.address
				cur_oracle.callproc("hrm_supp.update_attendance_activity", [k_attendance_id,k_latitude,k_longitude,l_location])
				print('Attendance location updated successfully.')
			except:
				k_latitude = tpl[0]
				k_longitude = tpl[1]
				k_attendance_id = tpl[2]
				print(k_latitude)
				print(k_longitude)
				print(k_attendance_id)
				location = geocoder.osm([k_latitude, k_longitude], method='reverse')
				print(location.address)
				if location.ok:
					cur_oracle.callproc("hrm_supp.update_attendance_activity", [k_attendance_id,k_latitude,k_longitude,location.address])
					print('Attendance location updated successfully.')
				else:
					cur_oracle.callproc("hrm_supp.update_attendance_activity", [k_attendance_id,k_latitude,k_longitude,"Address not found"])
					print('Attendance location update failed')
	except Exception as e:
		try:
			con = cx_Oracle.connect('u/p@ip/sid')
			cur_oracle = con.cursor()
		except Exception as e:
			pass

	time.sleep(10)
