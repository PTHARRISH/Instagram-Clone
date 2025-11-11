import React, { useMemo } from 'react';

/**
 * Optimized Reusable Input Component
 * Only shows error border and message when error exists
 * 
 * @param {string} type - Input type (text, email, password, etc.)
 * @param {string} name - Input name attribute
 * @param {string} label - Label text for the input
 * @param {string} placeholder - Placeholder text
 * @param {string} value - Input value
 * @param {Function} onChange - Change handler function
 * @param {string} error - Error message to display
 * @param {boolean} required - Whether the field is required
 * @param {string} autoComplete - Autocomplete attribute
 * @param {number} maxLength - Maximum length
 * @param {boolean} touched - Whether field has been touched/interacted with
 * @param {Object} rest - Other input props
 */
const Input = ({
  type = 'text',
  name,
  label,
  placeholder,
  value,
  onChange,
  error,
  required = false,
  autoComplete,
  maxLength,
  touched = true,
  ...rest
}) => {
  // Only show error styling if there's an error and field has been touched
  const showError = useMemo(() => touched && error, [touched, error]);

  return (
    <div className="w-full">
      {label && (
        <label
          htmlFor={name}
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          {label}
          {required && <span className="text-red-500 ml-1" aria-label="required">*</span>}
          {required && !showError && (
            <span className="text-gray-400 text-xs ml-2 font-normal">(required)</span>
          )}
        </label>
      )}
      
      <input
        type={type}
        id={name}
        name={name}
        value={value || ''}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        autoComplete={autoComplete}
        maxLength={maxLength}
        aria-invalid={showError}
        aria-describedby={showError ? `${name}-error` : undefined}
        className={`
          w-full px-4 py-2.5 border rounded-lg
          focus:outline-none focus:ring-2 focus:border-transparent
          transition-all duration-200 ease-in-out
          ${showError
            ? 'border-red-500 focus:ring-red-500' 
            : 'border-gray-300 hover:border-gray-400 focus:ring-blue-500'
          }
          ${rest.disabled ? 'bg-gray-100 cursor-not-allowed opacity-60' : 'bg-white'}
        `}
        {...rest}
      />
      
      {showError && (
        <p 
          id={`${name}-error`}
          className="mt-1.5 text-sm text-red-600 flex items-start"
          role="alert"
        >
          <svg
            className="w-4 h-4 mr-1.5 mt-0.5 flex-shrink-0"
            fill="currentColor"
            viewBox="0 0 20 20"
            aria-hidden="true"
          >
            <path
              fillRule="evenodd"
              d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
              clipRule="evenodd"
            />
          </svg>
          <span>{error}</span>
        </p>
      )}
    </div>
  );
};

export default Input;
