
DARK_BG = "#0f172a"  # Slate 900
SIDEBAR_BG = "#1e293b" # Slate 800
CARD_BG = "rgba(30, 41, 59, 0.7)"
ACCENT_CYAN = "#06b6d4" # Cyan 500
ACCENT_BLUE = "#3b82f6" # Blue 500
TEXT_MAIN = "#f8fafc" # Slate 50
TEXT_MUTED = "#94a3b8" # Slate 400

STYLESHEET = f"""
QMainWindow {{
    background-color: {DARK_BG};
    color: {TEXT_MAIN};
}}

QWidget {{
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
    color: {TEXT_MAIN};
}}

/* Sidebar */
QFrame#Sidebar {{
    background-color: {SIDEBAR_BG};
    border-right: 1px solid #334155;
}}

QLabel#Logo {{
    font-size: 20px;
    font-weight: bold;
    color: {ACCENT_CYAN};
    padding: 10px;
}}

QPushButton#NavButton {{
    background-color: transparent;
    border: none;
    text-align: left;
    padding: 10px 15px;
    color: {TEXT_MUTED};
    border-radius: 5px;
}}

QPushButton#NavButton:hover {{
    background-color: rgba(255, 255, 255, 0.05);
    color: {TEXT_MAIN};
}}

QPushButton#NavButton[active="true"] {{
    background-color: rgba(6, 182, 212, 0.15);
    color: {ACCENT_CYAN};
    border-left: 3px solid {ACCENT_CYAN};
}}

/* Cards */
QFrame#Card {{
    background-color: {SIDEBAR_BG}; 
    border-radius: 10px;
    border: 1px solid #334155;
}}

QLabel#CardTitle {{
    font-size: 16px;
    font-weight: bold;
    color: {TEXT_MAIN};
}}

QLabel#StatValue {{
    font-size: 24px;
    font-weight: bold;
    color: {TEXT_MAIN};
}}

QLabel#StatLabel {{
    font-size: 12px;
    color: {TEXT_MUTED};
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

/* Buttons */
QPushButton#PrimaryButton {{
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {ACCENT_BLUE}, stop:1 {ACCENT_CYAN});
    color: black;
    font-weight: bold;
    border-radius: 6px;
    padding: 10px 20px;
    border: none;
}}

QPushButton#PrimaryButton:hover {{
    opacity: 0.9;
}}

QPushButton#PrimaryButton:pressed {{
    background-color: {ACCENT_BLUE};
}}

QPushButton#DeleteButton {{
    background-color: transparent;
    border: none;
    color: {TEXT_MUTED};
}}

QPushButton#DeleteButton:hover {{
    color: #ff4d4d;
}}

/* Dialogs */
QMessageBox {{
    background-color: {SIDEBAR_BG};
    color: {TEXT_MAIN};
}}

QMessageBox QLabel {{
    color: {TEXT_MAIN};
}}

QMessageBox QPushButton {{
    background-color: {SIDEBAR_BG};
    border: 1px solid #334155;
    border-radius: 4px;
    padding: 6px 12px;
    color: {TEXT_MAIN};
    min-width: 60px;
}}

QMessageBox QPushButton:hover {{
    background-color: rgba(255, 255, 255, 0.05);
}}

QMessageBox QPushButton:pressed {{
    background-color: {ACCENT_BLUE};
    color: white;
    border: none;
}}

#DashboardView {{
    background-color: {DARK_BG};
}}

#DashboardContent {{
    background-color: {DARK_BG};
}}

#ExportButton {{
    background-color: {SIDEBAR_BG};
    color: {TEXT_MAIN};
    border: 1px solid #334155;
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: bold;
}}

#ExportButton:hover {{
    background-color: rgba(255, 255, 255, 0.05);
    border-color: {ACCENT_CYAN};
    color: {ACCENT_CYAN};
}}

QPushButton#SecondaryButton {{
    background-color: transparent;
    border: 1px solid {TEXT_MUTED};
    color: {TEXT_MUTED};
    font-weight: bold;
    border-radius: 6px;
    padding: 10px 20px;
}}

QPushButton#SecondaryButton:hover {{
    border-color: {TEXT_MAIN};
    color: {TEXT_MAIN};
    background-color: rgba(255, 255, 255, 0.05);
}}
"""
