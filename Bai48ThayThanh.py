import mysql.connector
from mysql.connector import Error
# Kết nối CSDL
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        database="studentmanagement",
        user="root",
        password="pipinp123A@"
    )

# Hàm in dữ liệu
def print_dataset(dataset):
    align = '{0:<3} {1:<6} {2:<15} {3:<10}'
    print(align.format('ID', 'Code','Name',"Age"))
    for item in dataset:
        id, code, name, age, avatar, intro = item
        print(align.format(id, code, name, age))

# 1. Lấy tất cả SV
def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student")
    dataset = cursor.fetchall()
    print("\n--- Tất cả sinh viên ---")
    print_dataset(dataset)
    cursor.close()
    conn.close()

# 2. SV từ 22-26 tuổi
def get_students_22_26():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student WHERE Age BETWEEN 22 AND 26")
    dataset = cursor.fetchall()
    print("\n--- SV tuổi từ 22 - 26 ---")
    print_dataset(dataset)
    cursor.close()
    conn.close()

# 3. Toàn bộ SV theo tuổi tăng dần
def get_students_order_age_asc():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student ORDER BY Age ASC")
    dataset = cursor.fetchall()
    print("\n--- SV theo tuổi tăng dần ---")
    print_dataset(dataset)
    cursor.close()
    conn.close()

# 4. SV 22-26 theo tuổi giảm dần
def get_students_22_26_desc():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student WHERE Age BETWEEN 22 AND 26 ORDER BY Age DESC")
    dataset = cursor.fetchall()
    print("\n--- SV 22 - 26 tuổi giảm dần ---")
    print_dataset(dataset)
    cursor.close()
    conn.close()

# 5. Truy vấn theo ID
def get_student_by_id(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student WHERE ID = %s", (student_id,))
    dataset = cursor.fetchone()
    if dataset:
        id, code, name, age, avatar, intro = dataset
        print("\n--- Thông tin SV theo ID ---")
        print("ID    =", id)
        print("Code  =", code)
        print("Name  =", name)
        print("Age   =", age)
    else:
        print("Không tìm thấy sinh viên ID =", student_id)
    cursor.close()
    conn.close()

#6. Chạy theo trang 
def get_students_limit_offset(limit, offset):
    conn = get_connection()
    cursor = conn.cursor()
    
    sql = "SELECT * FROM student LIMIT %s OFFSET %s"
    cursor.execute(sql, (limit, offset))
    
    dataset = cursor.fetchall()
    print(f"\n--- {limit} sinh viên (OFFSET {offset}) ---")
    print_dataset(dataset)

    cursor.close()
    conn.close()
#7. Thêm sinh viên
def insert_student(code, name, age):
    conn = get_connection()
    cursor = conn.cursor()
    
    sql = "INSERT INTO student (code, name, age) VALUES (%s, %s, %s)"
    val = (code, name, age)
    
    cursor.execute(sql, val)
    conn.commit()
    
    print(cursor.rowcount, "record inserted")
    
    cursor.close()
    conn.close()

#8. Thêm nhiều sinh viên
def insert_many_students(students):
    """
    students: danh sách tuple (code, name, age)
    """
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO student (code, name, age) VALUES (%s, %s, %s)"
    
    cursor.executemany(sql, students)
    conn.commit()
    
    print(cursor.rowcount, "records inserted")
    
    cursor.close()
    conn.close()

#9. Sửa thông tin sinh viên
def update_student_name_by_code(code, new_name):
    """
    Cập nhật cột name của sinh viên có Code = code thành new_name.
    Trả về số bản ghi bị ảnh hưởng (rowcount).
    """
    try:
        conn = get_connection()  # dùng hàm get_connection() bạn đã có
        cursor = conn.cursor()
        sql = "UPDATE student SET name = %s WHERE code = %s"
        val = (new_name, code)
        cursor.execute(sql, val)
        conn.commit()
        affected = cursor.rowcount
        print(f"{affected} record(s) affected")
        return affected
    except Error as e:
        # bạn có thể log lỗi vào file nếu muốn
        print("Lỗi khi cập nhật:", e)
        return 0
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass

#10. Del theo Id
def delete_student_by_id(student_id):
    """
    Xoá sinh viên theo ID.
    Trả về số bản ghi bị ảnh hưởng (rowcount).
    """
    try:
        conn = get_connection()   # dùng hàm get_connection() đã định nghĩa
        cursor = conn.cursor()
        
        sql = "DELETE FROM student WHERE ID = %s"
        cursor.execute(sql, (student_id,))
        
        conn.commit()
        affected = cursor.rowcount
        print(f"{affected} record(s) affected")
        return affected
    except Error as e:
        print("Lỗi khi xoá sinh viên:", e)
        return 0
    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass
#11. Del injection
def delete_student(student_id):
    """
    Xoá sinh viên theo ID.
    Trả về số bản ghi bị ảnh hưởng (rowcount).
    """
    try:
        conn = get_connection()   # dùng hàm get_connection() đã có
        cursor = conn.cursor()

        sql = "DELETE FROM student WHERE ID = %s"
        val = (student_id,)

        cursor.execute(sql, val)
        conn.commit()

        affected = cursor.rowcount
        print(f"{affected} record(s) affected")
        return affected
    except Error as e:
        print("Lỗi khi xoá sinh viên:", e)
        return 0
    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass

# Chạy
if __name__ == "__main__":
    delete_student_by_id(14)