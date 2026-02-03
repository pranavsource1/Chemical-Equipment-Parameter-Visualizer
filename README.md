# Chemical Equipment Visualizer

Hybrid Web Application for analyzing equipment parameters.

## Setup

### Backend
1. Open terminal in `backend` folder.
2. Initialize environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install django djangorestframework pandas matplotlib django-cors-headers
   ```
3. Run migrations and server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

### Frontend
1. Open new terminal in `frontend` folder.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start dev server:
   ```bash
   npm run dev
   ```

## Features
- **Upload**: Drag & Drop CSV upload.
- **Analytics**: Auto-calculation of Avg/Min/Max for Flowrate, Pressure, Temp.
- **Visuals**: Distribution and Trend charts.
- **History**: Tracks last 5 uploads.
- **Print**: Export dashboard to PDF via browser print.
