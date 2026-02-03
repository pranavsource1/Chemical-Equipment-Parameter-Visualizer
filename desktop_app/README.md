# Desktop Frontend

This folder contains the PyQt5 Desktop application for the Chem.Vis project.

## Features
- **Upload Dataset**: Drag-and-drop interface for CSV files.
- **Analytics Dashboard**: View stats, Matplotlib charts, and raw data tables.
- **History Management**: Sidebar navigation with auto-refresh and delete functionality.
- **PDF Export**: Save dashboard reports as PDF.
- **Modern UI**: Dark theme with glassmorphism effects.

## Setup & Run
1. Ensure the Django backend is running in another terminal:
   ```bash
   python manage.py runserver
   ```
2. Run the desktop app using the helper script:
   ```cmd
   ./run_desktop.bat
   ```
   Or manually:
   ```bash
   pip install -r desktop_app/requirements.txt
   python desktop_app/main.py
   ```
