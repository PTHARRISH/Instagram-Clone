# URL Verification & Connection Check

## ✅ Frontend Configuration

### Environment Variables
**File:** `frontend/.env` (Create this file if it doesn't exist)
```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

### API Configuration
**File:** `frontend/src/api/config.js`
- Base URL: `http://127.0.0.1:8000` (from env)
- API Base URL: `http://127.0.0.1:8000/api`
- Login Endpoint: `/login/`
- **Full Login URL:** `http://127.0.0.1:8000/api/login/`

### React Routes
**File:** `frontend/src/App.jsx`
- `/login` → Login page (public)
- `/` → Home page (protected)
- All other routes → Redirect to `/`

### Login Page
**File:** `frontend/src/pages/Login/Login.jsx`
- Uses `login()` from `api/auth.js`
- Calls: `POST http://127.0.0.1:8000/api/login/`
- Payload: `{ identifier: string, password: string }`

---

## ✅ Django Backend Configuration

### Settings
**File:** `backend/settings.py`
- ✅ CORS enabled for `localhost:5173` and `localhost:3000`
- ✅ JWT authentication configured
- ✅ Token blacklist enabled

### URL Routing
**File:** `backend/urls.py`
```
/api/ → includes api.urls
/api/token/refresh/ → TokenRefreshView
```

**File:** `api/urls.py`
```
/api/register/ → RegisterView
/api/login/ → LoginView
/api/logout/ → LogoutView
```

### API Endpoints Summary

| Endpoint | Method | View | Status |
|----------|--------|------|--------|
| `/api/register/` | POST | RegisterView | ✅ |
| `/api/login/` | POST | LoginView | ✅ |
| `/api/logout/` | POST | LogoutView | ✅ |
| `/api/token/refresh/` | POST | TokenRefreshView | ✅ |

---

## ✅ Connection Flow

### Login Request Flow:
1. **Frontend:** User submits login form
2. **React:** `Login.jsx` calls `login(identifier, password)`
3. **API Service:** `api/auth.js` calls `api.post('/login/', {...}, { skipAuth: true })`
4. **API Client:** `api/client.js` makes request to `http://127.0.0.1:8000/api/login/`
5. **Django:** Request hits `backend/urls.py` → `api/urls.py` → `LoginView`
6. **Django View:** `LoginView.post()` processes request, returns tokens
7. **Frontend:** Tokens stored in localStorage, user redirected to home

---

## 🔍 Testing Checklist

### 1. Create .env File
```bash
cd frontend
echo "VITE_API_BASE_URL=http://127.0.0.1:8000" > .env
```

### 2. Start Django Server
```bash
python manage.py runserver
# Server runs on http://127.0.0.1:8000
```

### 3. Start React Server
```bash
cd frontend
npm run dev
# Server runs on http://localhost:5173
```

### 4. Test Login
1. Open `http://localhost:5173/login`
2. Enter credentials (username/email/mobile + password)
3. Check browser console for errors
4. Check Django terminal for request logs

---

## 🐛 Troubleshooting

### If login doesn't work:

1. **Check .env file exists:**
   ```bash
   cat frontend/.env
   # Should show: VITE_API_BASE_URL=http://127.0.0.1:8000
   ```

2. **Check Django CORS settings:**
   - Verify `CORS_ALLOWED_ORIGINS` includes `http://localhost:5173`
   - Verify `corsheaders` is in `INSTALLED_APPS`
   - Verify `CorsMiddleware` is in `MIDDLEWARE`

3. **Check URL matches:**
   - Frontend calls: `http://127.0.0.1:8000/api/login/`
   - Django route: `/api/login/` → `LoginView`

4. **Check browser console:**
   - Look for CORS errors
   - Look for network errors
   - Check if request is being sent

5. **Check Django terminal:**
   - Should see debug print statements from `LoginView`
   - Should see request data

---

## 📝 Current Status

✅ Frontend routing configured
✅ Login page created
✅ API client configured
✅ Environment variables setup
✅ Django CORS configured
✅ Django URLs configured
✅ LoginView implemented

**Next Steps:**
1. Create `.env` file in `frontend/` directory
2. Start Django server: `python manage.py runserver`
3. Start React server: `npm run dev` (in frontend directory)
4. Test login at `http://localhost:5173/login`

