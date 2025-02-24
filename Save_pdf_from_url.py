import requests
url = 'http://192.168.188.26:8888/reports/rwservlet?melp&destype=cache&desformat=pdf&report=/home/oracle/test_source/hr_employee_wise_details.rdf&company=1&branch=01'
response = requests.get(url)
with open('sample.pdf', 'wb') as f:
    f.write(response.content)