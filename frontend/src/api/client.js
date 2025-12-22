import axios from 'axios';
import { API_ENDPOINTS } from './config';

// ========================================
// Token Management Functions
// ========================================

export const setTokens = (accessToken, refreshToken) => {
  if (accessToken) {
    localStorage.setItem('access_token', accessToken);
  }
  if (refreshToken) {
    localStorage.setItem('refresh_token', refreshToken);
  }
};

export const getAccessToken = () => {
  return localStorage.getItem('access_token');
};

export const getRefreshToken = () => {
  return localStorage.getItem('refresh_token');
};

export const clearTokens = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
};

export const isAuthenticated = () => {
  const token = getAccessToken();
  if (!token) return false;
  return !isTokenExpired();
};

export const isTokenExpired = () => {
  const token = getAccessToken();
  if (!token) return true;

  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const exp = payload.exp * 1000;
    const now = Date.now();
    return now >= exp;
  } catch (error) {
    console.error('[API] Error checking token expiry:', error);
    return true;
  }
};

export const refreshAccessToken = async () => {
  const refreshToken = getRefreshToken();

  if (!refreshToken) {
    clearTokens();
    throw new Error('No refresh token available');
  }

  try {
    const response = await axios.post(
      `${API_ENDPOINTS.BASE_URL}${API_ENDPOINTS.AUTH.REFRESH}`,
      { refresh: refreshToken }
    );

    const { access } = response.data;

    if (!access) {
      throw new Error('No access token in refresh response');
    }

    setTokens(access, refreshToken);
    return access;
  } catch (error) {
    console.error('[API] Token refresh failed:', error);
    clearTokens();
    throw error;
  }
};

// ========================================
// Axios Instance Configuration
// ========================================

const api = axios.create({
  baseURL: API_ENDPOINTS.BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ========================================
// Request Interceptor
// ========================================

api.interceptors.request.use(
  (config) => {
    const token = getAccessToken();

    if (token && !config.skipAuth) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// ========================================
// Response Interceptor
// ========================================

api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    if (originalRequest.skipAuth) {
      return Promise.reject(error);
    }

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const newAccessToken = await refreshAccessToken();
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return api(originalRequest);
      } catch (refreshError) {
        clearTokens();
        window.dispatchEvent(new CustomEvent('auth:logout'));
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;

