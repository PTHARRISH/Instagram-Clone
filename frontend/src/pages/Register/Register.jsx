import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import Input from '../../components/Input';
import { register } from '../../api/auth';
import { isAuthenticated } from '../../api/client';
import {
  validateFullName,
  validateUsername,
  validateEmail,
  validateMobile,
  validatePassword,
  validateConfirmPassword,
} from '../../utils/validation';

const Register = () => {
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    full_name: '',
    username: '',
    email: '',
    mobile: '',
    password: '',
    confirm_password: '',
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

    // Validate on blur using serializer-like validation
    let error = null;
    switch (name) {
      case 'full_name':
        error = validateFullName(formData.full_name);
        break;
      case 'username':
        error = validateUsername(formData.username);
        break;
      case 'email':
        error = validateEmail(formData.email);
        break;
      case 'mobile':
        error = validateMobile(formData.mobile);
        break;
      case 'password':
        error = validatePassword(formData.password);
        break;
      case 'confirm_password':
        error = validateConfirmPassword(formData.confirm_password, formData.password);
        break;
      default:
        break;
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
    const newTouched = {};

    // Validate all fields using serializer-like validation
    const fullNameError = validateFullName(formData.full_name);
    const usernameError = validateUsername(formData.username);
    const emailError = validateEmail(formData.email);
    const mobileError = validateMobile(formData.mobile);
    const passwordError = validatePassword(formData.password);
    const confirmPasswordError = validateConfirmPassword(
      formData.confirm_password,
      formData.password
    );

    if (fullNameError) newErrors.full_name = fullNameError;
    if (usernameError) newErrors.username = usernameError;
    if (emailError) newErrors.email = emailError;
    if (mobileError) newErrors.mobile = mobileError;
    if (passwordError) newErrors.password = passwordError;
    if (confirmPasswordError) newErrors.confirm_password = confirmPasswordError;

    // Mark all fields as touched
    Object.keys(formData).forEach((key) => {
      newTouched[key] = true;
    });

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
      // Trim all string fields before sending
      const trimmedData = {
        full_name: formData.full_name.trim(),
        username: formData.username.trim(),
        email: formData.email.trim(),
        mobile: formData.mobile.trim(),
        password: formData.password,
        confirm_password: formData.confirm_password,
      };

      await register(trimmedData);
      navigate('/login', {
        state: {
          message: 'Registration successful! Please login to continue.',
        },
        replace: true,
      });
    } catch (error) {
      console.error('Registration error:', error);
      
      // Handle backend serializer errors
      if (error.response?.data) {
        const errorData = error.response.data;
        const newErrors = {};
        
        // Map all serializer field errors
        const fieldMap = [
          'full_name',
          'username',
          'email',
          'mobile',
          'password',
          'confirm_password',
        ];

        fieldMap.forEach((field) => {
          if (errorData[field]) {
            newErrors[field] = Array.isArray(errorData[field])
              ? errorData[field][0]
              : errorData[field];
            setTouched((prev) => ({ ...prev, [field]: true }));
          }
        });

        setErrors((prev) => ({ ...prev, ...newErrors }));

        // General error message
        if (errorData.error || errorData.non_field_errors) {
          setGeneralError(
            errorData.error ||
              (Array.isArray(errorData.non_field_errors)
                ? errorData.non_field_errors[0]
                : errorData.non_field_errors) ||
              'Registration failed. Please check your information.'
          );
        } else if (Object.keys(newErrors).length === 0) {
          setGeneralError('Registration failed. Please try again.');
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
          <h2 className="text-4xl font-bold text-gray-900 mb-2">Create Account</h2>
          <p className="text-gray-600">Sign up to get started</p>
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

        {/* Registration Form */}
        <form onSubmit={handleSubmit} className="mt-8 space-y-4" noValidate>
          <Input
            type="text"
            name="full_name"
            label="Full Name"
            placeholder="Enter your full name"
            value={formData.full_name}
            onChange={handleChange}
            onBlur={handleBlur}
            error={errors.full_name}
            touched={touched.full_name}
            required
            autoComplete="name"
          />

          <Input
            type="text"
            name="username"
            label="Username"
            placeholder="Choose a username"
            value={formData.username}
            onChange={handleChange}
            onBlur={handleBlur}
            error={errors.username}
            touched={touched.username}
            required
            autoComplete="username"
          />

          <Input
            type="email"
            name="email"
            label="Email Address"
            placeholder="Enter your email"
            value={formData.email}
            onChange={handleChange}
            onBlur={handleBlur}
            error={errors.email}
            touched={touched.email}
            required
            autoComplete="email"
          />

          <Input
            type="tel"
            name="mobile"
            label="Mobile Number"
            placeholder="Enter 10-digit mobile number"
            value={formData.mobile}
            onChange={handleChange}
            onBlur={handleBlur}
            error={errors.mobile}
            touched={touched.mobile}
            required
            autoComplete="tel"
            maxLength={10}
          />

          <Input
            type="password"
            name="password"
            label="Password"
            placeholder="Create a password (min 8 characters)"
            value={formData.password}
            onChange={handleChange}
            onBlur={handleBlur}
            error={errors.password}
            touched={touched.password}
            required
            autoComplete="new-password"
          />

          <Input
            type="password"
            name="confirm_password"
            label="Confirm Password"
            placeholder="Re-enter your password"
            value={formData.confirm_password}
            onChange={handleChange}
            onBlur={handleBlur}
            error={errors.confirm_password}
            touched={touched.confirm_password}
            required
            autoComplete="new-password"
          />

          <button
            type="submit"
            disabled={isLoading}
            className={`
              w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-lg
              text-white font-medium text-lg mt-6
              ${isLoading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700'
              }
              focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500
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
                Creating account...
              </>
            ) : (
              'Create Account'
            )}
          </button>
        </form>

        {/* Login Link */}
        <div className="text-center mt-6">
          <p className="text-sm text-gray-600">
            Already have an account?{' '}
            <Link
              to="/login"
              className="font-medium text-blue-600 hover:text-blue-500"
            >
              Sign in here
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;
