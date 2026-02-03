
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QPushButton, QLabel, QFrame, QStackedWidget, QMessageBox, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, QTimer
from api_client import APIClient
from styles import STYLESHEET, ACCENT_CYAN
from upload_view import UploadView
from dashboard_view import DashboardView
from login_view import LoginView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chem.Vis Desktop")
        self.resize(1200, 800)
        self.api_client = APIClient()
        self.current_dataset_id = None
        self.datasets = []
        
        # Root Stack: Login vs Main App
        self.root_stack = QStackedWidget()
        self.setCentralWidget(self.root_stack)

        # 1. Login View
        self.login_view = LoginView(self.api_client)
        self.login_view.login_success.connect(self.handle_login_success)
        self.root_stack.addWidget(self.login_view)

        # 2. Main App Widget
        self.main_app_widget = QWidget()
        self.init_main_app_ui()
        self.root_stack.addWidget(self.main_app_widget)

        self.apply_styles()
        
        # Timer for polling (start only after login)
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_history)

    def apply_styles(self):
        self.setStyleSheet(STYLESHEET)

    def init_main_app_ui(self):
        main_layout = QHBoxLayout(self.main_app_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Sidebar ---
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(250)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 20)
        
        # Logo
        logo = QLabel("CHEM.VIS")
        logo.setObjectName("Logo")
        sidebar_layout.addWidget(logo)

        # Menu
        lbl_menu = QLabel(" MENU")
        lbl_menu.setStyleSheet("color: #94a3b8; font-size: 11px; margin-top: 20px; margin-left: 10px;")
        sidebar_layout.addWidget(lbl_menu)

        btn_new = QPushButton(" +  New Upload")
        btn_new.setObjectName("NavButton")
        btn_new.clicked.connect(self.show_upload)
        sidebar_layout.addWidget(btn_new)

        # History Section
        lbl_recent = QLabel(" RECENT DATASETS")
        lbl_recent.setStyleSheet("color: #94a3b8; font-size: 11px; margin-top: 20px; margin-left: 10px;")
        sidebar_layout.addWidget(lbl_recent)

        self.history_container = QWidget()
        self.history_layout = QVBoxLayout(self.history_container)
        self.history_layout.setContentsMargins(0,0,0,0)
        self.history_layout.setSpacing(2)
        sidebar_layout.addWidget(self.history_container)
        
        sidebar_layout.addStretch()
        
        # Logout Button
        btn_logout = QPushButton("Logout")
        btn_logout.setObjectName("NavButton")
        btn_logout.setStyleSheet("color: #ff4d4d; text-align: left; padding: 10px 15px;")
        btn_logout.clicked.connect(self.handle_logout)
        sidebar_layout.addWidget(btn_logout)

        main_layout.addWidget(self.sidebar)

        # --- Content Area ---
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        # Views
        self.upload_view = UploadView(self.api_client)
        self.upload_view.upload_success.connect(self.handle_upload_success)
        self.stack.addWidget(self.upload_view)

        self.dashboard_view = DashboardView(self.api_client)
        self.stack.addWidget(self.dashboard_view)

    def handle_login_success(self):
        self.root_stack.setCurrentWidget(self.main_app_widget)
        self.show_upload()
        self.timer.start(5000)
        self.refresh_history()

    def handle_logout(self):
        self.timer.stop()
        self.api_client.token = None
        self.root_stack.setCurrentWidget(self.login_view)
        
        # Reset specific states if needed
        self.datasets = []
        for i in reversed(range(self.history_layout.count())): 
             self.history_layout.itemAt(i).widget().setParent(None)

    def refresh_history(self):
        # Clear existing items
        for i in reversed(range(self.history_layout.count())): 
            self.history_layout.itemAt(i).widget().setParent(None)

        self.datasets = self.api_client.get_history()
        
        if not self.datasets:
            lbl = QLabel("No history yet.")
            lbl.setStyleSheet("color: #64748b; padding: 10px;")
            self.history_layout.addWidget(lbl)
            return

        for index, ds in enumerate(self.datasets):
            display_id = len(self.datasets) - index
            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(0, 0, 5, 0)
            
            # Nav Button
            btn = QPushButton(f" Dataset #{display_id}\n {ds['uploaded_at'][:10]}")
            btn.setObjectName("NavButton")
            btn.setProperty("active", str(self.current_dataset_id == ds['id']).lower())
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.clicked.connect(lambda checked, id=ds['id']: self.show_dashboard(id))
            item_layout.addWidget(btn)
            
            # Delete Button
            del_btn = QPushButton("🗑")
            del_btn.setObjectName("DeleteButton")
            del_btn.setFixedWidth(30)
            del_btn.clicked.connect(lambda checked, id=ds['id']: self.delete_dataset(id))
            item_layout.addWidget(del_btn)
            
            self.history_layout.addWidget(item_widget)

    def show_upload(self):
        self.current_dataset_id = None
        self.stack.setCurrentWidget(self.upload_view)
        self.refresh_history() # Update styling

    def show_dashboard(self, dataset_id):
        self.current_dataset_id = dataset_id
        self.stack.setCurrentWidget(self.dashboard_view)
        
        # Calculate display number
        display_number = "-"
        for i, ds in enumerate(self.datasets):
            if ds['id'] == dataset_id:
                display_number = str(len(self.datasets) - i)
                break
                
        self.dashboard_view.load_data(dataset_id, display_number)
        self.refresh_history() # Update styling

    def handle_upload_success(self, data):
        self.refresh_history()
        self.show_dashboard(data['id'])

    def delete_dataset(self, dataset_id):
        reply = QMessageBox.question(self, 'Delete Dataset', 
                                     "Are you sure you want to delete this dataset?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if self.api_client.delete_dataset(dataset_id):
                if self.current_dataset_id == dataset_id:
                    self.show_upload()
                else:
                    self.refresh_history()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
