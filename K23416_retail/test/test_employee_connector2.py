import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from connector.employee_connector import EmployeeConnector
from model.employee import Employee

ec = EmployeeConnector()
ec.connect()

# 🟦 Update
emp_update = Employee(ID=3, EmployeeCode="EX", Name="Con Cò",
                      Phone="3123123", Email="conco@example.com",
                      Password="654342423421", IsDeleted=0)
updated = ec.update_employee(emp_update)
print("Số dòng cập nhật:", updated)
