import { useEffect, useState } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { isAuthenticated, clearTokens } from '../api/client';

/**
 * ProtectedRoute Component
 * 
 * Protects routes that require authentication.
 * Redirects to login page if user is not authenticated.
 * 
 * @param {React.ReactNode} children - The component to render if authenticated
 * @param {string} redirectTo - The path to redirect to if not authenticated (default: '/login')
 */
const ProtectedRoute = ({ children, redirectTo = '/login' }) => {
  const [isAuth, setIsAuth] = useState(null); // null = checking, true/false = result
  const location = useLocation();

  useEffect(() => {
    // Check authentication status
    const checkAuth = () => {
      const authenticated = isAuthenticated();
      setIsAuth(authenticated);
      
      // If not authenticated, clear any stale tokens
      if (!authenticated) {
        clearTokens();
      }
    };

    // Initial check
    checkAuth();

    // Listen for auth logout events (from API interceptor)
    const handleAuthLogout = () => {
      setIsAuth(false);
    };

    window.addEventListener('auth:logout', handleAuthLogout);

    // Cleanup
    return () => {
      window.removeEventListener('auth:logout', handleAuthLogout);
    };
  }, []);

  // Show nothing while checking (or you can show a loading spinner)
  if (isAuth === null) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  // Redirect to login if not authenticated
  if (!isAuth) {
    return <Navigate to={redirectTo} state={{ from: location }} replace />;
  }

  // Render protected content
  return children;
};

export default ProtectedRoute;

