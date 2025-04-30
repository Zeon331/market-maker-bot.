from PyQt5 import QtWidgets, QtCore
from utils.logger import Logger

logger = Logger()

class LoginDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        try:
            self.setWindowTitle("Steam Login")
            self.setFixedSize(300, 150)
            
            self.txt_username = QtWidgets.QLineEdit()
            self.txt_password = QtWidgets.QLineEdit()
            self.txt_password.setEchoMode(QtWidgets.QLineEdit.Password)
            
            self.button_box = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
            )
            
            layout = QtWidgets.QFormLayout()
            layout.addRow("Username:", self.txt_username)
            layout.addRow("Password:", self.txt_password)
            layout.addWidget(self.button_box)
            
            self.button_box.accepted.connect(self.validate_input)
            self.button_box.rejected.connect(self.reject)
            
            self.setLayout(layout)
        except Exception as e:
            logger.error(f"LoginDialog init error: {str(e)}")
            raise

    def validate_input(self):
        try:
            if self.txt_username.text() and self.txt_password.text():
                self.accept()
            else:
                QtWidgets.QMessageBox.warning(
                    self, 
                    "Input Error", 
                    "Both fields are required!"
                )
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            self.reject()

    def get_credentials(self):
        return {
            "username": self.txt_username.text(),
            "password": self.txt_password.text()
        }

class SteamGuardDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        try:
            self.setWindowTitle("Steam Guard")
            self.setFixedSize(250, 120)
            
            self.txt_code = QtWidgets.QLineEdit()
            self.txt_code.setMaxLength(5)
            self.txt_code.setPlaceholderText("Enter 5-digit code")
            
            self.button_box = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
            )
            
            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(QtWidgets.QLabel("Steam Guard Code:"))
            layout.addWidget(self.txt_code)
            layout.addWidget(self.button_box)
            
            self.button_box.accepted.connect(self.accept)
            self.button_box.rejected.connect(self.reject)
            
            self.setLayout(layout)
        except Exception as e:
            logger.error(f"SteamGuardDialog init error: {str(e)}")
            raise

    def get_code(self):
        return self.txt_code.text()

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        try:
            self.setWindowTitle("Settings")
            self.setFixedSize(400, 300)
            
            self.txt_min_roi = QtWidgets.QLineEdit()
            self.txt_max_price = QtWidgets.QLineEdit()
            
            self.button_box = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
            )
            
            layout = QtWidgets.QFormLayout()
            layout.addRow("Minimum ROI (%):", self.txt_min_roi)
            layout.addRow("Maximum Price ($):", self.txt_max_price)
            layout.addWidget(self.button_box)
            
            self.button_box.accepted.connect(self.accept)
            self.button_box.rejected.connect(self.reject)
            
            self.setLayout(layout)
        except Exception as e:
            logger.error(f"SettingsDialog init error: {str(e)}")
            raise

    def get_settings(self):
        return {
            "min_roi": float(self.txt_min_roi.text()),
            "max_price": float(self.txt_max_price.text())
        }