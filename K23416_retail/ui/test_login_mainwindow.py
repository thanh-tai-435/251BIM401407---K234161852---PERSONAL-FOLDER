import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from PyQt6.QtWidgets import QApplication, QMainWindow

from K23416_retail.ui.LoginMainWindowEx import LoginMainWindowEx

app = QApplication([])
emp_ui = LoginMainWindowEx()
emp_ui.setupUi(QMainWindow())
emp_ui.showWindow()

app.exec()

