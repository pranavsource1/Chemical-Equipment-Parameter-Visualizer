import React, { useState } from 'react';
import { login } from '../services/api';
import { User, Lock, LogIn } from 'lucide-react';

const Login = ({ onLogin, onNavigateRegister }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        try {
            const res = await login(username, password);
            localStorage.setItem('access_token', res.data.access);
            localStorage.setItem('refresh_token', res.data.refresh);
            onLogin();
        } catch (err) {
            setError(err.response?.data?.detail || 'Login failed. Check credentials.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
            <div className="glass-card" style={{ padding: '2rem', width: '100%', maxWidth: '400px' }}>
                <h2 style={{ textAlign: 'center', marginBottom: '2rem' }}>Welcome Back</h2>

                <form onSubmit={handleSubmit}>
                    <div className="form-group" style={{ marginBottom: '1rem' }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-muted)' }}>Username</label>
                        <div style={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
                            <User size={18} style={{ position: 'absolute', left: '10px', color: 'var(--text-muted)' }} />
                            <input
                                type="text"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                style={{
                                    width: '100%',
                                    padding: '10px 10px 10px 35px',
                                    backgroundColor: 'rgba(255,255,255,0.05)',
                                    border: '1px solid #334155',
                                    borderRadius: '6px',
                                    color: 'white',
                                    outline: 'none'
                                }}
                                required
                            />
                        </div>
                    </div>

                    <div className="form-group" style={{ marginBottom: '1.5rem' }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-muted)' }}>Password</label>
                        <div style={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
                            <Lock size={18} style={{ position: 'absolute', left: '10px', color: 'var(--text-muted)' }} />
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                style={{
                                    width: '100%',
                                    padding: '10px 10px 10px 35px',
                                    backgroundColor: 'rgba(255,255,255,0.05)',
                                    border: '1px solid #334155',
                                    borderRadius: '6px',
                                    color: 'white',
                                    outline: 'none'
                                }}
                                required
                            />
                        </div>
                    </div>

                    {error && <div style={{ color: '#ff4d4d', marginBottom: '1rem', fontSize: '0.9rem' }}>{error}</div>}

                    <button
                        type="submit"
                        disabled={loading}
                        className="glass-card"
                        style={{
                            width: '100%',
                            padding: '12px',
                            background: 'var(--accent-cyan)',
                            color: 'black',
                            fontWeight: 'bold',
                            cursor: loading ? 'not-allowed' : 'pointer',
                            display: 'flex',
                            justifyContent: 'center',
                            alignItems: 'center',
                            gap: '8px'
                        }}
                    >
                        {loading ? 'Logging in...' : <><LogIn size={18} /> Login</>}
                    </button>

                    <div style={{ marginTop: '1.5rem', textAlign: 'center', fontSize: '0.9rem' }}>
                        <span style={{ color: 'var(--text-muted)' }}>Don't have an account? </span>
                        <a
                            href="#"
                            onClick={(e) => { e.preventDefault(); onNavigateRegister(); }}
                            style={{ color: 'var(--accent-cyan)', textDecoration: 'none' }}
                        >
                            Register
                        </a>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Login;
