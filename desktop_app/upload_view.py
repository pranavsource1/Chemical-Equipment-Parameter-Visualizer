
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QFrame, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from styles import ACCENT_CYAN, TEXT_MUTED

class UploadView(QWidget):
    upload_success = pyqtSignal(dict) # Emits dataset data on success

    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        # Title
        title = QLabel("Upload Equipment Data")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Upload a standard CSV file to generate analytics and visualizations.")
        subtitle.setStyleSheet(f"color: {TEXT_MUTED}; margin-bottom: 40px;")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        # Upload Area (Styled as a card)
        upload_card = QFrame()
        upload_card.setObjectName("Card") # Uses styles.py styling
        upload_card.setFixedSize(400, 250)
        
        card_layout = QVBoxLayout(upload_card)
        card_layout.setAlignment(Qt.AlignCenter)

        icon_label = QLabel("📄") # Placeholder for icon
        icon_label.setStyleSheet("font-size: 48px;")
        icon_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(icon_label)

        hint = QLabel("Drag & Drop your CSV file here\nor click to browse")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet(f"color: {TEXT_MUTED}; margin: 20px 0;")
        card_layout.addWidget(hint)

        self.btn_browse = QPushButton("Browse Files")
        self.btn_browse.setObjectName("PrimaryButton")
        self.btn_browse.setCursor(Qt.PointingHandCursor)
        self.btn_browse.clicked.connect(self.browse_file)
        card_layout.addWidget(self.btn_browse)

        layout.addWidget(upload_card)
        
        # CSV Instructions
        info_box = QFrame()
        info_box.setStyleSheet("background-color: rgba(255,255,255,0.05); border-radius: 8px; padding: 10px; margin-top: 20px;")
        info_layout = QHBoxLayout(info_box)
        info_lbl = QLabel("Required Columns: Equipment Name, Type, Flowrate, Pressure, Temperature")
        info_lbl.setStyleSheet(f"color: {ACCENT_CYAN}; font-size: 12px;")
        info_layout.addWidget(info_lbl)
        layout.addWidget(info_box)

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV Files (*.csv)")
        if file_name:
            self.upload_file(file_name)

    def upload_file(self, file_path):
        self.btn_browse.setText("Uploading...")
        self.btn_browse.setEnabled(False)
        
        try:
            data = self.api_client.upload_dataset(file_path)
            self.upload_success.emit(data)
        except Exception as e:
            self.btn_browse.setText("Upload Failed")
            print(e)
        finally:
            self.btn_browse.setEnabled(True)
            if self.btn_browse.text() != "Upload Failed":
                 self.btn_browse.setText("Browse Files")
