import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from connector.connector import Connector
from model.employee import Employee

class EmployeeConnector(Connector):
    def login(self, email, pwd):
        sql = '''
            SELECT * FROM employee WHERE Email = %s and Password = %s
        '''
        val = (email, pwd)
        dataset = self.fetchone(sql, val)
        if dataset == None:
            return None

        emp = Employee(dataset[0],
                       dataset[1],
                       dataset[2],
                       dataset[3],
                       dataset[4],
                       dataset[5],
                       dataset[6])
        return emp

    def get_all_employee(self):
        sql = "SELECT * FROM employee"
        self.connect()  # đảm bảo có kết nối
        datasets = self.fetchall(sql)  # không có giá trị truyền vào thì dùng tuple rỗng ()
        employees = []
        for dataset in datasets:
            emp = Employee(dataset[0],
                       dataset[1],
                       dataset[2],
                       dataset[3],
                       dataset[4],
                       dataset[5],
                       dataset[6])
            employees.append(emp)
        return employees
    
    def get_detail_infor(self,id):
        sql = '''
            SELECT * FROM employee WHERE ID = %s
        '''
        val = (id,)
        dataset = self.fetchone(sql, val)
        if dataset == None:
            return None

        emp = Employee(dataset[0],
                       dataset[1],
                       dataset[2],
                       dataset[3],
                       dataset[4],
                       dataset[5],
                       dataset[6])
        return emp
    def insert_employee(self, emp):
        sql = """
            INSERT INTO employee (EmployeeCode, Name, Phone, Email, Password, IsDeleted)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        val = (emp.EmployeeCode, emp.Name, emp.Phone, emp.Email, emp.Password, emp.IsDeleted)
        return self.execute(sql, val)
    def update_employee(self, emp):
        sql = """
            UPDATE employee
            SET EmployeeCode = %s,
                Name = %s,
                Phone = %s,
                Email = %s,
                Password = %s,
                IsDeleted = %s
            WHERE ID = %s
        """
        val = (emp.EmployeeCode, emp.Name, emp.Phone, emp.Email, emp.Password, emp.IsDeleted, emp.ID)
        result = self.update_employee(sql,val)
        return result
    def delete_one_employee(self,emp):
        sql = "delete from employee where ID = %s"
        val =(emp.ID,)
        result = self.update_employee(sql,val)
        return result
