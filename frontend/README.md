# React Frontend Application

## Project Structure

```
frontend/
├── src/
│   ├── api/                    # API layer
│   │   ├── config.js          # API configuration & endpoints
│   │   ├── client.js          # Axios instance & token management
│   │   ├── auth.js            # Authentication service
│   │   └── index.js           # API module exports
│   ├── components/            # Reusable components
│   │   ├── Input/             # Input component
│   │   │   ├── Input.jsx
│   │   │   └── index.js
│   │   └── ProtectedRoute.jsx # Route protection component
│   ├── pages/                 # Page components
│   │   └── Login/            # Login page
│   │       ├── Login.jsx
│   │       └── index.js
│   ├── assets/               # Static assets
│   ├── App.jsx               # Root component
│   ├── main.jsx             # Entry point
│   └── index.css            # Global styles
├── .env                      # Environment variables (create this file)
├── .gitignore               # Git ignore rules
└── package.json             # Dependencies
```

## Setup Instructions

### 1. Create Environment File

Create a `.env` file in the `frontend/` directory with the following content:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

**Note:** Vite requires the `VITE_` prefix for environment variables to be accessible in the app.

### 2. Install Dependencies

```bash
cd frontend
npm install
```

### 3. Run Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:5173` (default Vite port).

## API Configuration

The API base URL is configured in:
- **Environment Variable**: `VITE_API_BASE_URL` in `.env` file
- **Config File**: `src/api/config.js` - Centralized endpoint definitions
- **Client**: `src/api/client.js` - Axios instance with interceptors

## Components

### Input Component
Reusable input component with validation and error handling.

**Usage:**
```jsx
import Input from '../components/Input';

<Input
  type="text"
  name="username"
  label="Username"
  value={value}
  onChange={handleChange}
  error={errors.username}
  required
/>
```

### ProtectedRoute Component
Protects routes that require authentication.

**Usage:**
```jsx
import ProtectedRoute from './components/ProtectedRoute';

<Route
  path="/dashboard"
  element={
    <ProtectedRoute>
      <Dashboard />
    </ProtectedRoute>
  }
/>
```

## Authentication

Authentication is handled through the API layer:

```javascript
import { login, register, logout } from './api/auth';

// Login
await login(identifier, password);

// Register
await register(userData);

// Logout
await logout();
```

Tokens are automatically managed by the API client with automatic refresh on expiry.

## Environment Variables

All environment variables must be prefixed with `VITE_` to be accessible in the application:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Access in code:
```javascript
import.meta.env.VITE_API_BASE_URL
```
