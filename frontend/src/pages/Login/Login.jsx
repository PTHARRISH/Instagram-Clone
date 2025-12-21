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

  const handleChange = useCallback(
    (e) => {
      const { name, value } = e.target;

      setFormData((prev) => ({
        ...prev,
        [name]: value,
      }));

      if (!touched[name]) {
        setTouched((prev) => ({
          ...prev,
          [name]: true,
        }));
      }

      if (errors[name]) {
        setErrors((prev) => ({
          ...prev,
          [name]: '',
        }));
      }

      if (generalError) {
        setGeneralError('');
      }
    },
    [errors, touched, generalError]
  );

  const handleBlur = useCallback(
    (e) => {
      const { name } = e.target;

      if (!touched[name]) {
        setTouched((prev) => ({
          ...prev,
          [name]: true,
        }));
      }

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
    },
    [formData, touched]
  );

  const validateForm = useCallback(() => {
    const newErrors = {};
    const newTouched = { identifier: true, password: true };

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

    if (!validateForm()) return;

    setIsLoading(true);
    setGeneralError('');

    try {
      /**
       * BACKEND RESPONSE:
       * {
       *   message: "Login successful",
       *   username: "john_doe",
       *   tokens: { access, refresh }
       * }
       */
      const response = await login(
        formData.identifier.trim(),
        formData.password
      );

      const username = response?.username;

      if (!username) {
        throw new Error('Username not returned from server');
      }

      // ✅ REDIRECT TO PROFILE PAGE
      navigate(`/profile/${username}`, { replace: true });
    } catch (error) {
      console.error('Login error:', error);

      if (error.response?.data) {
        const errorData = error.response.data;

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

        if (errorData.error) {
          setGeneralError(errorData.error);
        } else if (errorData.non_field_errors) {
          setGeneralError(
            Array.isArray(errorData.non_field_errors)
              ? errorData.non_field_errors[0]
              : errorData.non_field_errors
          );
        } else {
          setGeneralError('Login failed. Please check your credentials.');
        }
      } else {
        setGeneralError('An unexpected error occurred. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 py-12 px-4">
      <div className="max-w-md w-full bg-white p-8 rounded-2xl shadow-2xl space-y-8">
        {/* Header */}
        <div className="text-center">
          <h2 className="text-4xl font-bold text-gray-900">Welcome Back</h2>
          <p className="text-gray-600 mt-1">
            Sign in to continue to Instagram
          </p>
        </div>

        {/* Error */}
        {generalError && (
          <div className="bg-red-50 border border-red-300 text-red-700 px-4 py-3 rounded-lg">
            {generalError}
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-6" noValidate>
          <Input
            type="text"
            name="identifier"
            label="Username, Email, or Mobile"
            placeholder="Enter your username, email, or mobile"
            value={formData.identifier}
            onChange={handleChange}
            onBlur={handleBlur}
            error={errors.identifier}
            touched={touched.identifier}
            required
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
          />

          <button
            type="submit"
            disabled={isLoading}
            className={`w-full py-3 rounded-lg text-white font-semibold transition
              ${
                isLoading
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:opacity-90'
              }`}
          >
            {isLoading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        {/* Footer */}
        <div className="text-center text-sm text-gray-600">
          Don’t have an account?{' '}
          <Link
            to="/register"
            className="text-blue-600 font-medium hover:underline"
          >
            Sign up
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Login;
