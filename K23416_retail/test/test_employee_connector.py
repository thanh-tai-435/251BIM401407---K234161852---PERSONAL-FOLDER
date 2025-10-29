from K23416_retail.connector.employee_connector import EmployeeConnector
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
ec = EmployeeConnector()
ec.connect()
em = ec.login("Putin@gmail.com", "123")
if em == None:
    print("Login Failed")
else:
    print("Login Succeeded")
    print(em)

print("List Of Employee")
ds = ec.get_all_employee()
print(ds)

id = 3
emp =ec.get_detail_infor(id)
if emp == None : 
    print(" k có nhân viên có mã = ", id)
else :
    print("có mã ,",id)
    print(emp)