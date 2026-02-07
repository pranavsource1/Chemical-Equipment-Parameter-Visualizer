import axios from 'axios';

const api = axios.create({
    baseURL: 'https://chemical-equipment-parameter-visualizer-hx5i.onrender.com/api/data',
    timeout: 10000,
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export const login = (username, password) => axios.post('https://chemical-equipment-parameter-visualizer-hx5i.onrender.com/api/data/token/', { username, password });
export const register = (username, password) => axios.post('https://chemical-equipment-parameter-visualizer-hx5i.onrender.com/api/data/register/', { username, password });

export const uploadDataset = (formData) => api.post('upload/', formData);
export const getHistory = () => api.get('history/');
export const getSummary = (id) => api.get(`summary/${id}/`);
export const deleteDataset = (id) => api.delete(`summary/${id}/`);

export default api;
