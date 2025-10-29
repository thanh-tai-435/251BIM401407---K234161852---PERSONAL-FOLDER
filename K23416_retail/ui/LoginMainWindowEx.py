from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QMainWindow
from K23416_retail.ui.LoginMainWindow import Ui_MainWindow
from K23416_retail.connector.employee_connector import EmployeeConnector
from K23416_retail.ui.EmployeeMainWindowEx import EmployeeMainWindowEx
class LoginMainWindowEx(Ui_MainWindow):
    def __init__(self):
        pass

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalandSlot()

    def showWindow(self):
        self.MainWindow.show()

    def setupSignalandSlot(self):
        self.pushButtonLogin.clicked.connect(self.processlogin)

    def processlogin(self):
        email = self.lineEditEmail.text()
        password = self.lineEditPassword.text()
        ec = EmployeeConnector()
        ec.connect()
        em = ec.login(email, password)
        if em == None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Login Failed!!!!")
            msg.setWindowTitle("Login Failed")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        else:
            self.gui_emp = EmployeeMainWindowEx()
            self.gui_emp.setupUi(QMainWindow())
            self.gui_emp.showWindow()
            
            self.MainWindow.close()