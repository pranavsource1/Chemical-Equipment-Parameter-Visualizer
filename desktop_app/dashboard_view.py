
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea, QSizePolicy, QPushButton, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtPrintSupport import QPrinter

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_facecolor('#1e293b') # Match sidebar/card bg
        self.axes = fig.add_subplot(111)
        self.axes.set_facecolor('#1e293b')
        super(MplCanvas, self).__init__(fig)

class DashboardView(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.dataset_id = None
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Scroll Area for the whole dashboard
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(20)
        
        scroll.setWidget(self.content_widget)
        self.main_layout.addWidget(scroll)

        # 1. Header
        header_layout = QHBoxLayout()
        self.content_layout.addLayout(header_layout)
        
        header_text_layout = QVBoxLayout()
        self.header_label = QLabel("Analytics Overview")
        self.header_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.sub_header_label = QLabel("Loading...")
        self.sub_header_label.setStyleSheet("color: #94a3b8;")
        header_text_layout.addWidget(self.header_label)
        header_text_layout.addWidget(self.sub_header_label)
        header_layout.addLayout(header_text_layout)
        
        header_layout.addStretch()
        
        self.btn_export = QPushButton("Export Report")
        self.btn_export.setObjectName("Card") # Reuse card style for simple look or define new
        self.btn_export.setStyleSheet("background-color: rgba(255,255,255,0.1); padding: 8px 16px; border-radius: 6px;")
        self.btn_export.clicked.connect(self.export_report)
        header_layout.addWidget(self.btn_export)

        # 2. Stats Grid
        self.stats_layout = QHBoxLayout()
        self.content_layout.addLayout(self.stats_layout)
        
        self.stat_cards = {}
        for key in ['total', 'flow', 'pressure', 'temp']:
            card = self.create_stat_card(key)
            self.stat_cards[key] = card
            self.stats_layout.addWidget(card['widget'])

        # 3. Charts Area
        charts_layout = QHBoxLayout()
        self.content_layout.addLayout(charts_layout)

        # Pie Chart Container
        self.dist_chart = MplCanvas(self, width=5, height=4, dpi=100)
        dist_container = self.create_chart_container("Equipment Distribution", self.dist_chart)
        charts_layout.addWidget(dist_container)

        # Line Chart Container
        self.trend_chart = MplCanvas(self, width=5, height=4, dpi=100)
        trend_container = self.create_chart_container("Parameter Trends (First 10)", self.trend_chart)
        charts_layout.addWidget(trend_container)

        # 4. Data Table
        self.table_label = QLabel("Raw Data Preview")
        self.table_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 20px;")
        self.content_layout.addWidget(self.table_label)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Type", "Flowrate", "Pressure", "Temp"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("""
            QTableWidget { background-color: #1e293b; border: 1px solid #334155; gridline-color: #334155; }
            QHeaderView::section { background-color: #0f172a; padding: 4px; border: none; font-weight: bold; }
            QTableCornerButton::section { background-color: #0f172a; }
        """)
        self.table.setMinimumHeight(300)
        self.content_layout.addWidget(self.table)

    def create_stat_card(self, key):
        frame = QFrame()
        frame.setObjectName("Card")
        layout = QVBoxLayout(frame)
        
        lbl_title = QLabel("TITLE")
        lbl_title.setObjectName("StatLabel")
        
        lbl_value = QLabel("-")
        lbl_value.setObjectName("StatValue")
        
        lbl_meta = QLabel("")
        lbl_meta.setStyleSheet("color: #94a3b8; font-size: 11px;")

        layout.addWidget(lbl_title)
        layout.addWidget(lbl_value)
        layout.addWidget(lbl_meta)
        
        return {'widget': frame, 'title': lbl_title, 'value': lbl_value, 'meta': lbl_meta}

    def create_chart_container(self, title_text, canvas):
        frame = QFrame()
        frame.setObjectName("Card")
        layout = QVBoxLayout(frame)
        
        title = QLabel(title_text)
        title.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 5px;")
        layout.addWidget(title)
        layout.addWidget(canvas)
        return frame

    def load_data(self, dataset_id, display_number=None):
        self.dataset_id = dataset_id
        self.display_number = display_number
        try:
            data = self.api_client.get_summary(dataset_id)
            self.last_data = data
            self.update_ui(data)
        except Exception as e:
            print(f"Error loading dashboard: {e}")

    def update_ui(self, data):
        summary = data['summary']
        raw_rows = data['data']
        
        display_id = self.display_number if self.display_number else data['dataset_id']
        self.sub_header_label.setText(f"Dataset #{display_id} • Imported on {data['uploaded_at'][:10]}")

        # Update Stats
        self.stat_cards['total']['title'].setText("Total Count")
        self.stat_cards['total']['value'].setText(str(summary['total_count']))
        
        self.update_stat_card(self.stat_cards['flow'], "Avg Flowrate", summary['flowrate'])
        self.update_stat_card(self.stat_cards['pressure'], "Avg Pressure", summary['pressure'])
        self.update_stat_card(self.stat_cards['temp'], "Avg Temp", summary['temperature'])

        # Update Pie Chart
        self.dist_chart.axes.clear()
        types = [d['equipment_type'] for d in summary['type_distribution']]
        counts = [d['count'] for d in summary['type_distribution']]
        # Dark theme styling for mpl
        text_props = {'color': 'white'}
        wedges, texts, autotexts = self.dist_chart.axes.pie(counts, labels=types, autopct='%1.1f%%', 
                                                            textprops=text_props, startangle=90)
        self.dist_chart.draw()

        # Update Trend Chart (Just plotting flowrate for now for simplicity, or multi-params)
        self.trend_chart.axes.clear()
        
        # Taking subset for clarity
        subset = raw_rows[:15] 
        names = [r['equipment_name'] for r in subset]
        flows = [r['flowrate'] for r in subset]
        
        self.trend_chart.axes.plot(names, flows, 'o-', color='#06b6d4', label='Flowrate')
        self.trend_chart.axes.tick_params(axis='x', rotation=45, colors='white')
        self.trend_chart.axes.tick_params(axis='y', colors='white')
        self.trend_chart.axes.spines['bottom'].set_color('#334155')
        self.trend_chart.axes.spines['top'].set_color('none') 
        self.trend_chart.axes.spines['left'].set_color('#334155')
        self.trend_chart.axes.spines['right'].set_color('none')
        self.trend_chart.axes.set_title("FlowRate by Equipment", color='white')
        self.trend_chart.figure.tight_layout()
        self.trend_chart.draw()

        # Update Table
        self.table.setRowCount(len(raw_rows))
        for i, row in enumerate(raw_rows):
            self.table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.table.setItem(i, 1, QTableWidgetItem(str(row['equipment_name'])))
            self.table.setItem(i, 2, QTableWidgetItem(str(row['equipment_type'])))
            self.table.setItem(i, 3, QTableWidgetItem(str(row['flowrate'])))
            self.table.setItem(i, 4, QTableWidgetItem(str(row['pressure'])))
            self.table.setItem(i, 5, QTableWidgetItem(str(row['temperature'])))

    def update_stat_card(self, card, title, stats):
        card['title'].setText(title)
        avg = stats.get('avg')
        card['value'].setText(f"{avg:.2f}" if avg is not None else "-")
        card['meta'].setText(f"Min: {stats.get('min', '-')} • Max: {stats.get('max', '-')}")

    def export_report(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Report", "", "PDF Files (*.pdf)")
        if not file_path:
            return

        try:
            from PyQt5.QtGui import QTextDocument, QImage
            from PyQt5.QtCore import QSizeF, QUrl, QDate
            import tempfile
            import os

            # 1. Save Charts to Temp Images
            dist_img_path = os.path.join(tempfile.gettempdir(), 'dist_chart.png')
            trend_img_path = os.path.join(tempfile.gettempdir(), 'trend_chart.png')
            
            # Save with specific face/edge colors for print (white background ideally for paper)
            # But user likes dark theme? Usually PDFs are white paper. 
            # Let's stick to standard white paper report for "proper pdf".
            # We temporarily change figure facecolor to white for export?
            # Or just keep it dark if that's the "aesthetic". 
            # User asked for "formatted and only data... not printscreen". 
            # Professional reports are usually white.
            
            orig_face_dist = self.dist_chart.figure.get_facecolor()
            self.dist_chart.figure.set_facecolor('white')
            self.dist_chart.axes.set_facecolor('white')
            # Fix text color for white bg? It might be white-on-white if not careful.
            # This is complex. For reliability, let's just save as is (Dark) for now, 
            # or try to enforce a style. 
            # Simpler: Just save as is. HTML styling handles the page.
            
            self.dist_chart.figure.savefig(dist_img_path, facecolor='#1e293b')
            self.trend_chart.figure.savefig(trend_img_path, facecolor='#1e293b')

            # 2. Prepare Data
            data = getattr(self, 'last_data', None)
            if not data:
                print("No data loaded to export.")
                return

            summary = data['summary']
            raw_rows = data['data']
            
            # 3. Build HTML
            # Using dark theme for PDF to match app aesthetic? Or standard white?
            # "Professional" usually implies white, but "Unique/High-end" might imply matching app.
            # I will go with a clean white paper look for the PDF itself for readability,
            # but keep the charts as they are (dark) which looks like "figures" inserted.
            
            html = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Helvetica, Arial, sans-serif; color: #333; }}
                    h1 {{ color: #0f172a; border-bottom: 2px solid #06b6d4; padding-bottom: 10px; }}
                    h2 {{ color: #334155; margin-top: 20px; }}
                    .meta {{ color: #64748b; font-size: 12px; margin-bottom: 20px; }}
                    .stats-grid {{ display: table; width: 100%; margin-bottom: 20px; }}
                    .stat-box {{ display: table-cell; width: 25%; padding: 10px; background: #f1f5f9; border: 1px solid #cbd5e1; text-align: center; }}
                    .stat-value {{ font-size: 18px; font-weight: bold; color: #0f172a; }}
                    .stat-label {{ font-size: 10px; color: #64748b; text-transform: uppercase; }}
                    
                    table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 10px; }}
                    th {{ background-color: #0f172a; color: white; padding: 5px; text-align: left; }}
                    td {{ border-bottom: 1px solid #e2e8f0; padding: 5px; }}
                    tr:nth-child(even) {{ background-color: #f8fafc; }}
                    
                    .chart-container {{ text-align: center; margin-top: 20px; page-break-inside: avoid; }}
                    img {{ width: 80%; height: auto; border: 1px solid #e2e8f0; }}
                </style>
            </head>
            <body>
                <h1>Chem.Vis Analytics Report</h1>
                <div class="meta">
                    <b>Dataset ID:</b> {data.get('dataset_id', '-')}<br>
                    <b>Imported:</b> {data.get('uploaded_at', '-')}<br>
                    <b>Generated:</b> {QDate.currentDate().toString(Qt.DefaultLocaleLongDate)}
                </div>

                <h2>Summary Statistics</h2>
                <div class="stats-grid">
                    <div class="stat-box">
                        <div class="stat-label">Total Valid Readings</div>
                        <div class="stat-value">{summary.get('total_count', 0)}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Avg Flowrate</div>
                        <div class="stat-value">{summary.get('flowrate', {}).get('avg', 0):.2f}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Avg Pressure</div>
                        <div class="stat-value">{summary.get('pressure', {}).get('avg', 0):.2f}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Avg Temperature</div>
                        <div class="stat-value">{summary.get('temperature', {}).get('avg', 0):.2f}</div>
                    </div>
                </div>

                <h2>Visualizations</h2>
                <div class="chart-container">
                    <h3>Equipment Distribution</h3>
                    <img src="{dist_img_path.replace(os.sep, '/')}">
                </div>
                <div class="chart-container">
                    <h3>Parameter Trends (Sample)</h3>
                    <img src="{trend_img_path.replace(os.sep, '/')}">
                </div>

                <h2>Raw Data (Top 50 Rows)</h2>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Equipment</th>
                            <th>Type</th>
                            <th>Flow</th>
                            <th>Pressure</th>
                            <th>Temp</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            
            for i, row in enumerate(raw_rows[:50]):
                html += f"""
                <tr>
                    <td>{i + 1}</td>
                    <td>{row.get('equipment_name', '-')}</td>
                    <td>{row.get('equipment_type', '-')}</td>
                    <td>{row.get('flowrate', '-')}</td>
                    <td>{row.get('pressure', '-')}</td>
                    <td>{row.get('temperature', '-')}</td>
                </tr>
                """
            
            html += """
                    </tbody>
                </table>
                <div style="text-align: center; color: #94a3b8; font-size: 10px; margin-top: 20px;">
                    Generated by Chem.Vis Desktop Application (Showing first 50 rows)
                </div>
            </body>
            </html>
            """

            # 4. Print
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(file_path)
            printer.setPageMargins(10, 10, 10, 10, QPrinter.Millimeter)

            doc = QTextDocument()
            doc.setHtml(html)
            doc.print_(printer)

            # Cleanup
            # if os.path.exists(dist_img_path): os.remove(dist_img_path)
            # if os.path.exists(trend_img_path): os.remove(trend_img_path)
            
            print(f"Report exported to {file_path}")

        except Exception as e:
            print(f"Export failed: {e}")
            import traceback
            traceback.print_exc()
