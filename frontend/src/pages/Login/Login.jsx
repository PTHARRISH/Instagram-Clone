import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import Input from '../../components/Input';
import { login } from '../../api/auth';
import { isAuthenticated } from '../../api/client';
import { validateIdentifier, validatePassword } from '../../utils/validation';

const Login = () => {
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    identifier: '',
    password: '',
  });
  
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [generalError, setGeneralError] = useState('');

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated()) {
      navigate('/', { replace: true });
    }
  }, [navigate]);

  const handleChange = useCallback((e) => {
    const { name, value } = e.target;
    
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    
    // Mark field as touched
    if (!touched[name]) {
      setTouched((prev) => ({
        ...prev,
        [name]: true,
      }));
    }
    
    // Clear field-specific error when user starts typing
    if (errors[name]) {
      setErrors((prev) => ({
        ...prev,
        [name]: '',
      }));
    }
    
    // Clear general error
    if (generalError) {
      setGeneralError('');
    }
  }, [errors, touched, generalError]);

  const handleBlur = useCallback((e) => {
    const { name } = e.target;
    
    // Mark field as touched
    if (!touched[name]) {
      setTouched((prev) => ({
        ...prev,
        [name]: true,
      }));
    }

    // Validate on blur
    let error = null;
    if (name === 'identifier') {
      error = validateIdentifier(formData.identifier);
    } else if (name === 'password') {
      error = validatePassword(formData.password);
    }

    if (error) {
      setErrors((prev) => ({
        ...prev,
        [name]: error,
      }));
    }
  }, [formData, touched]);

  const validateForm = useCallback(() => {
    const newErrors = {};
    const newTouched = { identifier: true, password: true };

    // Validate all fields
    const identifierError = validateIdentifier(formData.identifier);
    const passwordError = validatePassword(formData.password);

    if (identifierError) newErrors.identifier = identifierError;
    if (passwordError) newErrors.password = passwordError;

    setErrors(newErrors);
    setTouched((prev) => ({ ...prev, ...newTouched }));
    
    return Object.keys(newErrors).length === 0;
  }, [formData]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    setGeneralError('');

    try {
      await login(formData.identifier.trim(), formData.password);
      navigate('/', { replace: true });
    } catch (error) {
      console.error('Login error:', error);
      
      // Handle backend serializer errors
      if (error.response?.data) {
        const errorData = error.response.data;
        
        // Map serializer field errors
        if (errorData.identifier) {
          setErrors((prev) => ({
            ...prev,
            identifier: Array.isArray(errorData.identifier) 
              ? errorData.identifier[0] 
              : errorData.identifier,
          }));
          setTouched((prev) => ({ ...prev, identifier: true }));
        }
        
        if (errorData.password) {
          setErrors((prev) => ({
            ...prev,
            password: Array.isArray(errorData.password) 
              ? errorData.password[0] 
              : errorData.password,
          }));
          setTouched((prev) => ({ ...prev, password: true }));
        }
        
        // General errors
        if (errorData.error) {
          setGeneralError(errorData.error);
        } else if (errorData.non_field_errors) {
          setGeneralError(
            Array.isArray(errorData.non_field_errors)
              ? errorData.non_field_errors[0]
              : errorData.non_field_errors
          );
        } else if (!errorData.identifier && !errorData.password) {
          setGeneralError('Login failed. Please check your credentials.');
        }
      } else if (error.message) {
        setGeneralError(error.message);
      } else {
        setGeneralError('An unexpected error occurred. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 bg-white p-8 rounded-2xl shadow-2xl">
        {/* Header */}
        <div className="text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-2">Welcome Back</h2>
          <p className="text-gray-600">Sign in to your account</p>
        </div>

        {/* General Error Message */}
        {generalError && (
          <div className="bg-red-50 border-2 border-red-300 text-red-700 px-4 py-3 rounded-lg" role="alert">
            <div className="flex items-center">
              <svg
                className="w-5 h-5 mr-2 text-red-500 flex-shrink-0"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clipRule="evenodd"
                />
              </svg>
              <span className="font-medium">{generalError}</span>
            </div>
          </div>
        )}

        {/* Login Form */}
        <form onSubmit={handleSubmit} className="mt-8 space-y-6" noValidate>
          <Input
            type="text"
            name="identifier"
            label="Username, Email, or Mobile"
            placeholder="Enter your username, email, or mobile number"
            value={formData.identifier}
            onChange={handleChange}
            onBlur={handleBlur}
            error={errors.identifier}
            touched={touched.identifier}
            required
            autoComplete="username"
          />

          <Input
            type="password"
            name="password"
            label="Password"
            placeholder="Enter your password"
            value={formData.password}
            onChange={handleChange}
            onBlur={handleBlur}
            error={errors.password}
            touched={touched.password}
            required
            autoComplete="current-password"
          />

          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <input
                id="remember-me"
                name="remember-me"
                type="checkbox"
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-900">
                Remember me
              </label>
            </div>

            <div className="text-sm">
              <Link
                to="/forgot-password"
                className="font-medium text-blue-600 hover:text-blue-500"
              >
                Forgot password?
              </Link>
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className={`
              w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-lg
              text-white font-medium text-lg
              ${isLoading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700'
              }
              focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500
              transition-all transform hover:scale-105 disabled:transform-none
            `}
          >
            {isLoading ? (
              <>
                <svg
                  className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                Signing in...
              </>
            ) : (
              'Sign in'
            )}
          </button>
        </form>

        {/* Register Link */}
        <div className="text-center mt-6">
          <p className="text-sm text-gray-600">
            Don't have an account?{' '}
            <Link
              to="/register"
              className="font-medium text-blue-600 hover:text-blue-500"
            >
              Sign up here
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
