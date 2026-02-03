import React, { useEffect, useState } from 'react';
import { getSummary } from '../services/api';
import { TypeDistributionChart, ParameterChart } from './Charts';
import { Loader2, TrendingUp, Activity, Thermometer, Droplets } from 'lucide-react';

import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import html2canvas from 'html2canvas';

const DashboardView = ({ datasetId, datasetNumber }) => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [exporting, setExporting] = useState(false);

    useEffect(() => {
        if (!datasetId) return;
        const fetchData = async () => {
            setLoading(true);
            try {
                const res = await getSummary(datasetId);
                setData(res.data);
                setError(null);
            } catch (err) {
                console.error(err);
                setError('Failed to load dataset summary.');
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [datasetId]);

    const handleExport = async () => {
        if (!data) return;
        setExporting(true);
        try {
            const doc = new jsPDF();
            const { summary, data: rawRows } = data;

            // 1. Header & Styles
            doc.setFontSize(22);
            doc.setTextColor(15, 23, 42); // slate-900
            doc.text("Chem.Vis Analytics Report", 14, 20);

            doc.setDrawColor(6, 182, 212); // cyan
            doc.setLineWidth(1);
            doc.line(14, 25, 196, 25);

            // 2. Metadata
            doc.setFontSize(10);
            doc.setTextColor(100, 116, 139); // slate-500
            doc.text(`Dataset ID: ${datasetNumber}`, 14, 32);
            doc.text(`Imported: ${new Date(data.uploaded_at).toLocaleDateString()}`, 14, 37);
            doc.text(`Generated: ${new Date().toLocaleDateString()}`, 14, 42);

            // 3. Stats Grid (Manual drawing)
            let yPos = 55;
            doc.setFontSize(14);
            doc.setTextColor(51, 65, 85);
            doc.text("Summary Statistics", 14, yPos);
            yPos += 10;

            const stats = [
                { label: "Total Count", value: summary.total_count },
                { label: "Avg Flowrate", value: summary.flowrate.avg?.toFixed(2) },
                { label: "Avg Pressure", value: summary.pressure.avg?.toFixed(2) },
                { label: "Avg Temp", value: summary.temperature.avg?.toFixed(2) }
            ];

            stats.forEach((stat, i) => {
                const x = 14 + (i * 45);
                doc.setFillColor(241, 245, 249); // slate-100
                doc.setDrawColor(203, 213, 225); // slate-300
                doc.rect(x, yPos, 40, 20, 'FD');

                doc.setFontSize(8);
                doc.setTextColor(100, 116, 139);
                doc.text(stat.label, x + 20, yPos + 6, { align: 'center' });

                doc.setFontSize(12);
                doc.setFont("helvetica", "bold");
                doc.setTextColor(15, 23, 42);
                doc.text(String(stat.value), x + 20, yPos + 15, { align: 'center' });
            });

            yPos += 30;

            // 4. Charts - Capture from DOM
            doc.setFontSize(14);
            doc.setFont("helvetica", "normal");
            doc.setTextColor(51, 65, 85);
            doc.text("Visualizations", 14, yPos);
            yPos += 10;

            const chart1 = document.getElementById('chart-dist');
            const chart2 = document.getElementById('chart-trend');

            // Helper to capture chart
            const addChartToDoc = async (element, x, y, w, h) => {
                try {
                    if (element) {
                        const canvas = await html2canvas(element, { scale: 2, backgroundColor: '#1e293b' });
                        const img = canvas.toDataURL('image/png');
                        doc.addImage(img, 'PNG', x, y, w, h);
                    }
                } catch (e) {
                    console.warn("Chart capture failed", e);
                }
            };

            await addChartToDoc(chart1, 14, yPos, 85, 60);
            await addChartToDoc(chart2, 105, yPos, 90, 60);

            yPos += 70;

            // 5. Data Table
            doc.text("Raw Data Preview", 14, yPos);
            autoTable(doc, {
                startY: yPos + 5,
                head: [['ID', 'Equipment', 'Type', 'Flow', 'Pressure', 'Temp']],
                body: rawRows.slice(0, 50).map((row, i) => [
                    i + 1,
                    row.equipment_name,
                    row.equipment_type,
                    row.flowrate,
                    row.pressure,
                    row.temperature
                ]),
                theme: 'grid',
                headStyles: { fillColor: [15, 23, 42] },
                styles: { fontSize: 8 },
                didDrawPage: (data) => {
                    // Optional: Footer or page number
                }
            });

            doc.save(`Report_Dataset_${datasetNumber}.pdf`);

        } catch (err) {
            console.error("Export failed detailed:", err);
            alert("Failed to generate PDF. check console.");
        } finally {
            setExporting(false);
        }
    };

    if (loading) return (
        <div style={{ display: 'flex', justifyContent: 'center', padding: '4rem' }}>
            <Loader2 className="animate-spin" size={40} color="var(--accent-cyan)" />
        </div>
    );

    if (error) return <div style={{ color: '#ff4d4d', padding: '2rem' }}>{error}</div>;
    if (!data) return null;

    const { summary, data: rawData } = data;

    return (
        <div className="animate-fade-in">
            <div className="header">
                <div>
                    <h2 className="page-title">Analytics Overview</h2>
                    <p style={{ color: 'var(--text-muted)' }}>Dataset #{datasetNumber} • Imported on {new Date(data.uploaded_at).toLocaleDateString()}</p>
                </div>
                <button
                    className="glass-card"
                    onClick={handleExport}
                    disabled={exporting}
                    style={{ cursor: exporting ? 'wait' : 'pointer', padding: '0.5rem 1rem', background: exporting ? 'rgba(255,255,255,0.1)' : undefined }}
                >
                    {exporting ? 'Generating...' : 'Export PDF Report'}
                </button>
            </div>

            <div className="stats-grid" style={{ marginBottom: '2rem' }}>
                <div className="glass-card">
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <Activity color="#4facfe" />
                        <span className="stat-label">Total Count</span>
                    </div>
                    <div className="stat-value">{summary.total_count}</div>
                </div>

                <div className="glass-card">
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <Droplets color="#00f2ea" />
                        <span className="stat-label">Avg Flowrate</span>
                    </div>
                    <div className="stat-value">{summary.flowrate.avg?.toFixed(2) || '-'}</div>
                    <small style={{ color: 'var(--text-muted)' }}>Min: {summary.flowrate.min} • Max: {summary.flowrate.max}</small>
                </div>

                <div className="glass-card">
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <Activity color="#f093fb" />
                        <span className="stat-label">Avg Pressure</span>
                    </div>
                    <div className="stat-value">{summary.pressure.avg?.toFixed(2) || '-'}</div>
                    <small style={{ color: 'var(--text-muted)' }}>Min: {summary.pressure.min} • Max: {summary.pressure.max}</small>
                </div>

                <div className="glass-card">
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <Thermometer color="#ff6b6b" />
                        <span className="stat-label">Avg Temp</span>
                    </div>
                    <div className="stat-value">{summary.temperature.avg?.toFixed(2) || '-'}</div>
                    <small style={{ color: 'var(--text-muted)' }}>Min: {summary.temperature.min} • Max: {summary.temperature.max}</small>
                </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '2rem' }}>
                <div className="glass-card">
                    <h4 style={{ marginBottom: '1rem' }}>Equipment Type Distribution</h4>
                    <div className="chart-container" id="chart-dist">
                        <TypeDistributionChart data={summary.type_distribution} />
                    </div>
                </div>
                <div className="glass-card">
                    <h4 style={{ marginBottom: '1rem' }}>Parameter Trends</h4>
                    <div className="chart-container" id="chart-trend">
                        <ParameterChart rawData={rawData} />
                    </div>
                </div>
            </div>

            <div className="glass-card">
                <h4 style={{ marginBottom: '1rem' }}>Raw Data Preview</h4>
                <div style={{ overflowX: 'auto' }}>
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Equipment Name</th>
                                <th>Type</th>
                                <th>Flowrate</th>
                                <th>Pressure</th>
                                <th>Temperature</th>
                            </tr>
                        </thead>
                        <tbody>
                            {rawData.slice(0, 10).map((row, index) => (
                                <tr key={row.id}>
                                    <td>{index + 1}</td>
                                    <td>{row.equipment_name}</td>
                                    <td>{row.equipment_type}</td>
                                    <td>{row.flowrate}</td>
                                    <td>{row.pressure}</td>
                                    <td>{row.temperature}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                    {rawData.length > 10 && <p style={{ padding: '1rem', textAlign: 'center', color: 'var(--text-muted)' }}>Showing 10 of {rawData.length} rows</p>}
                </div>
            </div>
        </div>
    );
};

export default DashboardView;
