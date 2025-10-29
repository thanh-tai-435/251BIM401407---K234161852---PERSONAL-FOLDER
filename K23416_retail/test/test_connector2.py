import traceback
import mysql.connector

server = "localhost"
port =  3306
database = "k23416_retail"
user = "root"
password  = "pipinp123A@"

try:
    conn =  mysql.connector.connect(
        host = server,
        port = port,
        database = database,
        user = user,
        password = password,
    )
except:
    traceback.print_exc()
print("Continue...")
print("CRUD")

def login_customer(email, pwd):
    cursor = conn.cursor()
    sql = "SELECT * FROM customer WHERE Email='"+email +"' and Password='"+pwd+"'"
    print(sql)
    cursor.execute(sql)
    data = cursor.fetchone()
    if data != None:
        print(data)
    else:
        print("Login Failed")
    cursor.close()
login_customer("camdao@gmail.com", "123")

def login_employee(email, pwd):
    cursor = conn.cursor()
    sql = "SELECT * FROM employee WHERE Email=%s and Password=%s"
    val = (email, pwd)
    cursor.execute(sql, val)
    data = cursor.fetchone()
    if data != None:
        print(data)
    else:
        print("Login Failed")
    cursor.close()
login_employee("Obama@gmail.com", "123")