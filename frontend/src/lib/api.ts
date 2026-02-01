
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        if (error.response && error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            try {
                const refreshToken = localStorage.getItem('refreshToken');
                if (!refreshToken) {
                    // No refresh token, force logout
                    localStorage.removeItem('token');
                    window.location.href = '/auth/login';
                    return Promise.reject(error);
                }

                const res = await axios.post(`${API_URL}/auth/refresh`, {}, {
                    headers: { Authorization: `Bearer ${refreshToken}` }
                });

                if (res.status === 200) {
                    localStorage.setItem('token', res.data.access_token);
                    api.defaults.headers.common['Authorization'] = `Bearer ${res.data.access_token}`;
                    return api(originalRequest);
                }
            } catch (err) {
                // Refresh failed
                localStorage.removeItem('token');
                localStorage.removeItem('refreshToken');
                window.location.href = '/auth/login';
            }
        }
        return Promise.reject(error);
    }
);

export default api;
