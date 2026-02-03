import React, { useEffect, useState } from 'react';
import { LayoutDashboard, History, FileText, PlusCircle, Trash2 } from 'lucide-react';
import { getHistory, deleteDataset } from '../services/api';

const Sidebar = ({ history, onSelectDataset, onNewUpload, currentId, onDatasetDeleted, onLogout }) => {

    const handleDelete = async (e, id) => {
        e.stopPropagation();
        if (window.confirm('Are you sure you want to delete this dataset?')) {
            try {
                await deleteDataset(id);
                if (onDatasetDeleted) onDatasetDeleted(id);
            } catch (err) {
                console.error("Failed to delete dataset", err);
                alert("Failed to delete dataset");
            }
        }
    };

    return (
        <div className="sidebar">
            <div className="logo">
                CHEM.VIS
            </div>

            <div className="nav-group">
                <h4 style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginBottom: '1rem', textTransform: 'uppercase' }}>Menu</h4>

                <div className="nav-item" onClick={onNewUpload}>
                    <PlusCircle size={18} />
                    <span>New Upload</span>
                </div>
            </div>

            <div className="nav-group" style={{ marginTop: '2rem' }}>
                <h4 style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginBottom: '1rem', textTransform: 'uppercase' }}>Recent Datasets</h4>

                {history.map((item, index) => {
                    const displayId = history.length - index;
                    return (
                        <div
                            key={item.id}
                            className={`nav-item ${currentId === item.id ? 'active' : ''}`}
                            onClick={() => onSelectDataset(item.id)}
                            style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingRight: '8px' }}
                        >
                            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', overflow: 'hidden' }}>
                                <FileText size={16} style={{ flexShrink: 0 }} />
                                <span style={{ fontSize: '0.9rem', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                                    Dataset #{displayId}
                                    <br />
                                    <span style={{ fontSize: '0.7rem', opacity: 0.6 }}>
                                        {new Date(item.uploaded_at).toLocaleDateString()}
                                    </span>
                                </span>
                            </div>
                            <button
                                className="delete-btn"
                                onClick={(e) => handleDelete(e, item.id)}
                                style={{
                                    background: 'transparent',
                                    border: 'none',
                                    color: 'var(--text-muted)',
                                    cursor: 'pointer',
                                    padding: '4px',
                                    borderRadius: '4px',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center'
                                }}
                                onMouseEnter={(e) => e.currentTarget.style.color = '#ff4d4d'}
                                onMouseLeave={(e) => e.currentTarget.style.color = 'var(--text-muted)'}
                                title="Delete Dataset"
                            >
                                <Trash2 size={14} />
                            </button>
                        </div>
                    );
                })}

                {history.length === 0 && (
                    <div style={{ padding: '1rem', color: 'var(--text-muted)', fontSize: '0.9rem', fontStyle: 'italic' }}>
                        No history yet.
                    </div>
                )}
            </div>

            <div style={{ marginTop: 'auto' }}>
                <div
                    className="glass-card nav-item"
                    onClick={onLogout}
                    style={{ padding: '0.8rem 1rem', background: 'rgba(255, 77, 77, 0.1)', border: '1px solid rgba(255, 77, 77, 0.2)', color: '#ff4d4d', cursor: 'pointer', justifyContent: 'center' }}
                >
                    <span style={{ fontWeight: 'bold', fontSize: '0.9rem' }}>Logout</span>
                </div>
            </div>
        </div>
    );
};

export default Sidebar;
