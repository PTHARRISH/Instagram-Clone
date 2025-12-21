const Button = ({ children, variant = 'primary', ...props }) => {
  const styles = {
    primary:
      'bg-blue-600 hover:bg-blue-700 text-white',
    secondary:
      'border border-gray-300 hover:bg-gray-100 text-gray-900',
    danger:
      'bg-red-600 hover:bg-red-700 text-white',
  };

  return (
    <button
      {...props}
      className={`px-4 py-1.5 rounded-lg font-medium transition ${styles[variant]}`}
    >
      {children}
    </button>
  );
};

export default Button;
