import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import UploadDataset from './components/UploadDataset';
import DashboardView from './components/DashboardView';
import Login from './components/Login';
import Register from './components/Register';
import { getHistory } from './services/api';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isRegistering, setIsRegistering] = useState(false);
  const [currentDatasetId, setCurrentDatasetId] = useState(null);
  const [view, setView] = useState('upload'); // 'upload' or 'dashboard'
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) setIsAuthenticated(true);
  }, []);

  const fetchHistory = async () => {
    try {
      const res = await getHistory();
      setHistory(res.data);
    } catch (err) {
      console.error(err);
      if (err.response && err.response.status === 401) {
        handleLogout();
      }
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      fetchHistory();
      const interval = setInterval(fetchHistory, 5000);
      return () => clearInterval(interval);
    }
  }, [isAuthenticated]);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setIsAuthenticated(false);
    setHistory([]);
    setCurrentDatasetId(null);
    setView('upload');
  };

  const handleUploadSuccess = (data) => {
    fetchHistory();
    setCurrentDatasetId(data.id);
    setView('dashboard');
  };

  const handleSelectDataset = (id) => {
    setCurrentDatasetId(id);
    setView('dashboard');
  };

  const handleDatasetDeleted = (deletedId) => {
    if (currentDatasetId === deletedId) {
      setCurrentDatasetId(null);
      setView('upload');
    }
    fetchHistory();
  };

  // Calculate display number (Newest is at index 0, so number = length - index)
  const activeIndex = history.findIndex(item => item.id === currentDatasetId);
  const activeDatasetNumber = activeIndex !== -1 ? history.length - activeIndex : '-';

  if (!isAuthenticated) {
    if (isRegistering) return <Register onNavigateLogin={() => setIsRegistering(false)} />;
    return <Login onLogin={() => setIsAuthenticated(true)} onNavigateRegister={() => setIsRegistering(true)} />;
  }

  return (
    <div className="app-container">
      <Sidebar
        history={history}
        currentId={currentDatasetId}
        onSelectDataset={handleSelectDataset}
        onNewUpload={() => setView('upload')}
        onDatasetDeleted={handleDatasetDeleted}
        onLogout={handleLogout}
      />

      <main className="main-content">
        {view === 'upload' && (
          <div style={{ maxWidth: '600px', margin: '4rem auto', width: '100%' }}>
            <h1 className="page-title" style={{ textAlign: 'center', marginBottom: '2rem' }}>
              Upload Equipment Data
            </h1>
            <p style={{ textAlign: 'center', color: 'var(--text-muted)', marginBottom: '3rem' }}>
              Upload a standard CSV file to generate analytics and visualizations for your chemical equipment parameters.
            </p>
            <UploadDataset onUploadSuccess={handleUploadSuccess} />
          </div>
        )}

        {view === 'dashboard' && (
          <DashboardView
            datasetId={currentDatasetId}
            datasetNumber={activeDatasetNumber}
          />
        )}
      </main>
    </div>
  );
}

export default App;
