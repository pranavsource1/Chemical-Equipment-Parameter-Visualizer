from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal

class LoginView(QWidget):
    login_success = pyqtSignal()

    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        # Container Card
        card = QFrame()
        card.setObjectName("Card")
        card.setFixedWidth(350)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(20)
        card_layout.setContentsMargins(30, 40, 30, 40)

        # Title
        title = QLabel("Log In")
        title.setObjectName("CardTitle")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; margin-bottom: 20px;")
        card_layout.addWidget(title)
        
        # Username
        lbl_user = QLabel("Username")
        lbl_user.setObjectName("StatLabel")
        self.input_user = QLineEdit()
        self.input_user.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #334155;
                border-radius: 5px;
                background-color: rgba(255, 255, 255, 0.05);
                color: white;
            }
        """)
        card_layout.addWidget(lbl_user)
        card_layout.addWidget(self.input_user)

        # Password
        lbl_pass = QLabel("Password")
        lbl_pass.setObjectName("StatLabel")
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)
        self.input_pass.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #334155;
                border-radius: 5px;
                background-color: rgba(255, 255, 255, 0.05);
                color: white;
            }
        """)
        card_layout.addWidget(lbl_pass)
        card_layout.addWidget(self.input_pass)

        # Error Msg
        self.lbl_error = QLabel("")
        self.lbl_error.setStyleSheet("color: #ff4d4d; font-size: 12px;")
        self.lbl_error.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.lbl_error)

        # Button
        self.btn_login = QPushButton("Sign In")
        self.btn_login.setObjectName("PrimaryButton")
        self.btn_login.clicked.connect(self.handle_login)
        card_layout.addWidget(self.btn_login)

        layout.addWidget(card)

    def handle_login(self):
        username = self.input_user.text()
        password = self.input_pass.text()
        
        self.btn_login.setText("Signing In...")
        self.btn_login.setEnabled(False)
        self.lbl_error.setText("")

        # Force UI update needed? usually processEvents if blocking, but requests is blocking.
        # Ideally threading, but for simple task keep main thread blocked briefly.
        import PyQt5.QtWidgets
        PyQt5.QtWidgets.QApplication.processEvents()
        
        if self.api_client.login(username, password):
            self.login_success.emit()
        else:
            self.lbl_error.setText("Invalid credentials or server error.")
            self.btn_login.setText("Sign In")
            self.btn_login.setEnabled(True)
    def reset_ui(self):
        self.input_user.clear()
        self.input_pass.clear()
        self.btn_login.setText("Sign In")
        self.btn_login.setEnabled(True)
        self.lbl_error.setText("")
