# connector_sakila.py
import mysql.connector
import traceback
import pandas as pd

class Connector:
    def __init__(self,
                 server="localhost",
                 port=3306,
                 database="sakila",     # ⚡ đổi sang sakila
                 username="root",
                 password="pipinp123A@"):
        self.server = server
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.conn = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.server,
                port=self.port,
                database=self.database,
                user=self.username,
                password=self.password
            )
            return self.conn
        except:
            self.conn = None
            traceback.print_exc()
        return None

    def disConnect(self):
        if self.conn:
            self.conn.close()

    def queryDataset(self, sql):
        try:
            if not self.conn or not self.conn.is_connected():
                self.connect()
            cursor = self.conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            df = pd.DataFrame(rows)
            if not df.empty:
                df.columns = cursor.column_names
            return df
        except Exception as e:
            print("❌ [DEBUG] Lỗi khi truy vấn MySQL:", e)
            traceback.print_exc()
            return None

    def getTablesName(self):
        cursor = self.conn.cursor()
        cursor.execute("SHOW TABLES;")
        results = cursor.fetchall()
        return [item[0] for item in results]

    def fetchone(self, sql, val):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, val)
            return cursor.fetchone()
        except:
            traceback.print_exc()
        return None

    def fetchall(self, sql, val=None):
        try:
            cursor = self.conn.cursor()
            if val:
                cursor.execute(sql, val)
            else:
                cursor.execute(sql)
            return cursor.fetchall()
        except:
            traceback.print_exc()
        return None

    def execute(self, sql, val=None):
        try:
            if not self.conn:
                self.connect()
            cursor = self.conn.cursor()
            if val:
                cursor.execute(sql, val)
            else:
                cursor.execute(sql)
            self.conn.commit()
            return cursor.lastrowid or 0
        except Exception as e:
            traceback.print_exc()
            self.conn.rollback()
            print("❌ Lỗi khi execute:", e)
            return 0
        finally:
            cursor.close()
