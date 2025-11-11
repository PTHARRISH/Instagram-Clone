/**
 * API Configuration
 * Reads base URL from environment variables
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export const API_ENDPOINTS = {
  BASE_URL: `${API_BASE_URL}/api`,
  AUTH: {
    LOGIN: '/login/',
    REGISTER: '/register/',
    LOGOUT: '/logout/',
    REFRESH: '/token/refresh/',
    USER_INFO: '/user/',
  },
};

export default API_ENDPOINTS;

