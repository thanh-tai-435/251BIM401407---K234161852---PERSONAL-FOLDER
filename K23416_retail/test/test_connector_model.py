import traceback
import mysql.connector

from K23416_retail.model.customer import Customer

server = "localhost"
port =  3306
database = "k23416_retail"
user = "root"
password  = "@Obama123"

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

def login_customer(email, pwd):
    cursor = conn.cursor()
    sql = "SELECT * FROM customer WHERE Email=%s AND Password=%s"
    val = (email, pwd)
    cust = None
    cursor.execute(sql, val)
    data = cursor.fetchone()
    if data != None:
        cust=Customer(*data)
    cursor.close()
    return cust
cust = login_customer("camdao@gmail.com", "123")
if cust == None:
    print("Login Failed")
else:
    print("Login Succeeded")
    print(cust)
