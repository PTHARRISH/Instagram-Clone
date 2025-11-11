/**
 * Validation utilities that mirror backend serializer validation rules
 * This ensures frontend and backend validation are consistent
 */

/**
 * Validate email format (mirrors backend RegisterSerializer.validate_email)
 */
export const validateEmail = (email) => {
  if (!email || !email.trim()) {
    return 'Email is required';
  }

  const trimmedEmail = email.trim();

  if (trimmedEmail.length < 5) {
    return 'Email is too short';
  }

  if (!trimmedEmail.includes('@')) {
    return 'Enter a valid email address';
  }

  if (trimmedEmail.split('@').length !== 2) {
    return 'Enter a valid email address';
  }

  const emailRegex = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
  if (!emailRegex.test(trimmedEmail)) {
    return 'Enter a valid email address';
  }

  return null;
};

/**
 * Validate mobile number (mirrors backend RegisterSerializer.validate_mobile)
 */
export const validateMobile = (mobile) => {
  if (!mobile || !mobile.trim()) {
    return 'Mobile number is required';
  }

  const mobileStr = String(mobile).trim();

  if (mobileStr.length < 10) {
    return 'Mobile number must be at least 10 digits';
  }

  if (!/^\d+$/.test(mobileStr)) {
    return 'Mobile number must contain only digits';
  }

  if (mobileStr.length > 10) {
    return 'Mobile number must be exactly 10 digits';
  }

  return null;
};

/**
 * Validate password (mirrors backend RegisterSerializer.validate_password)
 */
export const validatePassword = (password) => {
  if (!password || !password.trim()) {
    return 'Password is required';
  }

  if (password.length < 8) {
    return 'Password must be at least 8 characters long';
  }

  // Check for at least one letter, digit, or special character
  if (!/[a-zA-Z0-9_.+-]/.test(password)) {
    return 'Password must contain at least one letter, digit, or special character';
  }

  return null;
};

/**
 * Validate identifier for login (mirrors backend LoginSerializer.validate_identifier)
 */
export const validateIdentifier = (identifier) => {
  if (!identifier || !identifier.trim()) {
    return 'Username, email, or mobile number is required';
  }
  return null;
};

/**
 * Validate full name
 */
export const validateFullName = (fullName) => {
  if (!fullName || !fullName.trim()) {
    return 'Full name is required';
  }

  if (fullName.trim().length < 2) {
    return 'Full name must be at least 2 characters';
  }

  return null;
};

/**
 * Validate username
 */
export const validateUsername = (username) => {
  if (!username || !username.trim()) {
    return 'Username is required';
  }

  if (username.trim().length < 3) {
    return 'Username must be at least 3 characters';
  }

  return null;
};

/**
 * Validate confirm password
 */
export const validateConfirmPassword = (confirmPassword, password) => {
  if (!confirmPassword || !confirmPassword.trim()) {
    return 'Please confirm your password';
  }

  if (confirmPassword !== password) {
    return 'Passwords do not match';
  }

  return null;
};

