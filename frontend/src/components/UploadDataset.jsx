import React, { useState, useRef } from 'react';
import { Upload, FileText, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import { uploadDataset } from '../services/api';

const UploadDataset = ({ onUploadSuccess }) => {
    const [dragActive, setDragActive] = useState(false);
    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState(null);
    const inputRef = useRef(null);

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0]);
        }
    };

    const handleChange = (e) => {
        e.preventDefault();
        if (e.target.files && e.target.files[0]) {
            handleFile(e.target.files[0]);
        }
    };

    const handleFile = (file) => {
        if (file.type !== 'text/csv' && !file.name.endsWith('.csv')) {
            setError('Only CSV files are allowed.');
            return;
        }
        setFile(file);
        setError(null);
    };

    const handleSubmit = async () => {
        if (!file) return;
        setUploading(true);
        setError(null);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const res = await uploadDataset(formData);
            setFile(null);
            if (onUploadSuccess) onUploadSuccess(res.data);
        } catch (err) {
            console.error(err);
            setError('Upload failed. Please check the file format.');
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="glass-card">
            <h3 style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '10px' }}>
                <Upload size={20} color="var(--accent-cyan)" /> Update Data Source
            </h3>

            <div
                className={`upload-zone ${dragActive ? 'drag-active' : ''}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                onClick={() => inputRef.current.click()}
            >
                <input
                    ref={inputRef}
                    type="file"
                    accept=".csv"
                    onChange={handleChange}
                    style={{ display: 'none' }}
                />

                {!file ? (
                    <>
                        <p style={{ color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
                            Drag & Drop your CSV file here
                        </p>
                        <p style={{ fontSize: '0.8rem', opacity: 0.6 }}>or click to browse</p>
                    </>
                ) : (
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px' }}>
                        <FileText size={24} color="var(--accent-blue)" />
                        <span>{file.name}</span>
                        <CheckCircle size={16} color="var(--accent-cyan)" />
                    </div>
                )}
            </div>

            {error && (
                <div style={{ marginTop: '1rem', color: '#ff4d4d', display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.9rem' }}>
                    <AlertCircle size={16} /> {error}
                </div>
            )}

            {file && (
                <button
                    onClick={(e) => { e.stopPropagation(); handleSubmit(); }}
                    disabled={uploading}
                    style={{
                        marginTop: '1.5rem',
                        width: '100%',
                        padding: '0.8rem',
                        background: 'linear-gradient(90deg, var(--accent-blue), var(--accent-cyan))',
                        border: 'none',
                        borderRadius: '8px',
                        color: '#000',
                        fontWeight: '600',
                        cursor: uploading ? 'not-allowed' : 'pointer',
                        opacity: uploading ? 0.7 : 1,
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        gap: '8px'
                    }}
                >
                    {uploading ? <Loader2 className="animate-spin" size={18} /> : 'Process Dataset'}
                </button>
            )}

            <div style={{ marginTop: '1.5rem', padding: '1rem', background: 'rgba(255,255,255,0.05)', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)' }}>
                <h4 style={{ fontSize: '0.9rem', marginBottom: '0.5rem', color: 'var(--accent-cyan)', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <FileText size={16} /> Required CSV Format
                </h4>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', lineHeight: '1.4' }}>
                    Your CSV file must include these columns:<br />
                    <code style={{ color: 'var(--accent-blue)', background: 'rgba(0,0,0,0.2)', padding: '2px 4px', borderRadius: '4px', display: 'inline-block', marginTop: '4px' }}>
                        Equipment Name, Type, Flowrate, Pressure, Temperature
                    </code>
                </p>
            </div>
        </div>
    );
};

export default UploadDataset;
