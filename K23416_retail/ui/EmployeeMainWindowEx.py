from PyQt6.QtWidgets import *
from K23416_retail.ui.EmployeeMainWindow import Ui_MainWindow
from K23416_retail.test.test_employee_connector import EmployeeConnector
from K23416_retail.model.employee import Employee

class EmployeeMainWindowEx(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ec = EmployeeConnector()
        self.ec.connect()
        self.is_completed = False  # ✅ Trạng thái kiểm tra tổng thể

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.displayEmployeesTable()
        self.setupSignalAndSlot()
        self.is_completed = True  # ✅ UI setup thành công

    def showWindow(self):
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        self.pushButtonNew.clicked.connect(self.clear_all)
        self.tableWidgetEmployee.itemSelectionChanged.connect(self.show_detail)
        self.pushButtonUpdate.clicked.connect(self.update_employee)
        self.pushButtonSave.clicked.connect(self.save_employee)  # ✅ bổ sung nút save nếu có

    # ========================== LOGIN ==========================
    def processlogin(self):
        self.is_completed = False
        email = self.lineEditEmail.text()
        password = self.lineEditPassword.text()
        try:
            ec = EmployeeConnector()
            ec.connect()
            em = ec.login(email, password)
            if em is None:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setText("Login Failed!")
                msg.setWindowTitle("Login Error")
                msg.exec()
            else:
                self.gui_emp = EmployeeMainWindowEx()
                win = QMainWindow()
                self.gui_emp.setupUi(win)
                self.gui_emp.showWindow()
                self.MainWindow.close()
                self.is_completed = True
        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Error", f"Lỗi khi đăng nhập: {e}")

    # ========================== CLEAR ==========================
    def clear_all(self):
        self.lineEditID.clear()
        self.lineEditCode.clear()
        self.lineEditName.clear()
        self.lineEditPhone.clear()
        self.lineEditEmail.clear()
        self.lineEditPassword.clear()
        self.lineEditCode.setFocus()
        self.is_completed = True

    # ========================== DISPLAY TABLE ==========================
    def displayEmployeesTable(self):
        try:
            self.employees = self.ec.get_all_employee()
            self.tableWidgetEmployee.setRowCount(0)
            for emp in self.employees:
                row = self.tableWidgetEmployee.rowCount()
                self.tableWidgetEmployee.insertRow(row)
                self.tableWidgetEmployee.setItem(row, 0, QTableWidgetItem(str(emp.ID)))
                self.tableWidgetEmployee.setItem(row, 1, QTableWidgetItem(emp.EmployeeCode))
                self.tableWidgetEmployee.setItem(row, 2, QTableWidgetItem(emp.Name))
                self.tableWidgetEmployee.setItem(row, 3, QTableWidgetItem(emp.Phone))
                self.tableWidgetEmployee.setItem(row, 4, QTableWidgetItem(emp.Email))
            self.is_completed = True
        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Lỗi", f"Không thể load dữ liệu nhân viên: {e}")

    # ========================== SHOW DETAIL ==========================
    def show_detail(self):
        try:
            row_index = self.tableWidgetEmployee.currentIndex().row()
            if row_index < 0:
                return
            emp_id = self.tableWidgetEmployee.item(row_index, 0).text()
            emp = self.ec.get_detail_infor(emp_id)
            if emp:
                self.lineEditID.setText(str(emp.ID))
                self.lineEditCode.setText(emp.EmployeeCode)
                self.lineEditEmail.setText(emp.Email)
                self.lineEditName.setText(emp.Name)
                self.lineEditPhone.setText(emp.Phone)
                self.checkBoxIsDeleted.setChecked(bool(emp.IsDeleted))
                self.is_completed = True
        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Lỗi", f"Không thể hiển thị chi tiết nhân viên: {e}")

    # ========================== SAVE ==========================
    def save_employee(self):
        try:
            emp = Employee()
            emp.Name = self.lineEditName.text()
            emp.EmployeeCode = self.lineEditCode.text()
            emp.Email = self.lineEditEmail.text()
            emp.Password = self.lineEditPassword.text()
            emp.IsDeleted = 0

            result = self.ec.insert_employee(emp)
            if result and result > 0:
                QMessageBox.information(self.MainWindow, "Thành công", f"Đã thêm nhân viên {emp.Name}")
                self.displayEmployeesTable()
                self.is_completed = True
            else:
                QMessageBox.critical(self.MainWindow, "Lỗi", "Không thể thêm nhân viên. Kiểm tra dữ liệu nhập.")
        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Lỗi", f"Lỗi khi thêm nhân viên: {e}")

    # ========================== UPDATE ==========================
    def update_employee(self):
        try:
            emp = Employee()
            emp.ID = self.lineEditID.text()
            emp.Name = self.lineEditName.text()
            emp.EmployeeCode = self.lineEditCode.text()
            emp.Email = self.lineEditEmail.text()
            emp.Password = self.lineEditPassword.text()
            emp.IsDeleted = 1 if self.checkBoxIsDeleted.isChecked() else 0

            result = self.ec.update_employee(emp)
            if result and result > 0:
                QMessageBox.information(self.MainWindow, "Thành công", f"Đã cập nhật nhân viên {emp.Name}")
                self.displayEmployeesTable()
                self.is_completed = True
            else:
                QMessageBox.critical(self.MainWindow, "Lỗi", "Không thể cập nhật nhân viên.")
        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Lỗi", f"Lỗi khi cập nhật nhân viên: {e}")
    # - Delete EmPLoyEE
    def delete_employee(self):
        self.is_completed = False
        emp = Employee()
        emp.ID = self.lineEditID.text()
        result = self.ec.delete_one_employee(emp)
        if result > 0 : 
            self.displayEmployeesTable()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText