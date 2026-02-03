import React from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Bar, Line } from 'react-chartjs-2';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    Title,
    Tooltip,
    Legend
);

const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'top',
            labels: {
                color: '#94a3b8',
                font: { family: 'Outfit', size: 12 }
            }
        },
        tooltip: {
            backgroundColor: 'rgba(10, 21, 37, 0.9)',
            titleColor: '#fff',
            bodyColor: '#e0f2fe',
            borderColor: 'rgba(255,255,255,0.1)',
            borderWidth: 1,
            padding: 12,
            cornerRadius: 8
        }
    },
    scales: {
        x: {
            grid: { color: 'rgba(255,255,255,0.05)' },
            ticks: { color: '#94a3b8' }
        },
        y: {
            grid: { color: 'rgba(255,255,255,0.05)' },
            ticks: { color: '#94a3b8' }
        }
    }
};

export const TypeDistributionChart = ({ data }) => {
    if (!data) return null;

    const chartData = {
        labels: data.map(d => d.equipment_type),
        datasets: [
            {
                label: 'Equipment Count',
                data: data.map(d => d.count),
                backgroundColor: 'rgba(0, 242, 234, 0.5)',
                borderColor: '#00f2ea',
                borderWidth: 1,
                borderRadius: 4,
            },
        ],
    };

    return <Bar options={commonOptions} data={chartData} />;
};

export const ParameterChart = ({ rawData }) => {
    if (!rawData) return null;
    // Limit to first 20 for readability if too large
    const displayData = rawData.slice(0, 30);

    const chartData = {
        labels: displayData.map(d => d.equipment_name),
        datasets: [
            {
                label: 'Flowrate',
                data: displayData.map(d => d.flowrate),
                borderColor: '#4facfe',
                backgroundColor: 'rgba(79, 172, 254, 0.2)',
                tension: 0.4,
            },
            {
                label: 'Pressure',
                data: displayData.map(d => d.pressure),
                borderColor: '#f093fb',
                backgroundColor: 'rgba(240, 147, 251, 0.2)',
                tension: 0.4,
            }
        ],
    };

    return <Line options={commonOptions} data={chartData} />;
};
