import api, { setTokens, clearTokens, getRefreshToken } from './client';
import { API_ENDPOINTS } from './config';

/**
 * Authentication Service
 * Handles all authentication-related API calls
 */

/**
 * Register a new user
 * @param {Object} userData - User registration data
 * @returns {Promise<Object>} Registration response
 */
export const register = async (userData) => {
  try {
    const response = await api.post(API_ENDPOINTS.AUTH.REGISTER, userData, {
      skipAuth: true,
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Login user with identifier (username, email, or mobile) and password
 * @param {string} identifier - Username, email, or mobile number
 * @param {string} password - User password
 * @returns {Promise<Object>} Login response with tokens and user info
 */
export const login = async (identifier, password) => {
  try {
    const response = await api.post(
      API_ENDPOINTS.AUTH.LOGIN,
      { identifier, password },
      { skipAuth: true }
    );

    const { tokens } = response.data;
    if (tokens?.access && tokens?.refresh) {
      setTokens(tokens.access, tokens.refresh);
    }

    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Logout user (blacklists refresh token)
 * @returns {Promise<Object>} Logout response
 */
export const logout = async () => {
  try {
    const refreshToken = getRefreshToken();
    
    if (refreshToken) {
      await api.post(API_ENDPOINTS.AUTH.LOGOUT, { refresh: refreshToken });
    }
    
    clearTokens();
    return { message: 'Logout successful' };
  } catch (error) {
    clearTokens();
    throw error;
  }
};

/**
 * Get current user information
 * @returns {Promise<Object>} User information
 */
export const getUserInfo = async () => {
  try {
    const response = await api.get(API_ENDPOINTS.AUTH.USER_INFO);
    return response.data;
  } catch (error) {
    throw error;
  }
};

