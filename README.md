# Instagram Clone

A Django REST Framework microservice that handles all user-related functionalities similar to Instagram, including authentication, profiles, followers/following, blocking/muting, close friends, user settings, and permission management.

---

## Features

### 1. Authentication & Authorization
- **User Registration** (`RegisterView`): Sign up with `username`, `email`, `mobile`, `full_name`, and `password`.
- **Login** (`LoginView`): Login using `username`, `email`, or `mobile`.
- **Logout** (`LogoutView`): Blacklist refresh tokens for secure logout.
- **Delete Account** (`DeleteAccountView`): Delete account via signed URL with 24-hour expiry.

### 2. Profile Management
- **Profile CRUD** (`ProfileView`):
  - Retrieve and update user profiles.
  - Profiles include bio, avatar, gender, website, and privacy settings.
- **Follower/Following Counts**: Annotated dynamically.

### 3. Followers & Following
- **List Followers** (`FollowersView`)
- **List Following** (`FollowingView`)
- **Follow/Unfollow Actions** (`FollowActionView`)
- **Follow Requests** (`FollowRequestRespondView`)
- Supports search and pagination.

### 4. Blocking & Muting
- **Block Users** (`BlockedUser` / `BlockUserView`)
- **Mute Users** (`MutedUser` / `MuteUserView`)
- Granular mute options: posts and stories.

### 5. Close Friends
- **Manage Close Friends** (`CloseFriend` / `CloseFriendView`)
- Users can add or remove close friends for selective content sharing.

### 6. User Settings
- **Settings per User** (`UserSettings` / `UserSettingsView`)
- Options include:
  - Allow messages from followers
  - Show activity status
  - Allow mentions

### 7. RBAC (Role-Based Access Control)
- **Roles** (`Role`) and **Page Permissions** (`PagePermission`)
- Assign permissions dynamically to users (`AssignUserPermissionView`)
- **DynamicPagePermission**: Restricts API access based on HTTP method and URL permission settings.
- Admin endpoints explicitly use `IsAdminUser`.

---

## API Endpoints Overview

### Auth
| Endpoint | Method | Permission | Description |
|----------|--------|-----------|-------------|
| `/api/register/` | POST | Public | User registration |
| `/api/login/` | POST | Public | Login with username/email/mobile |
| `/api/logout/` | POST | Authenticated | Logout and blacklist refresh token |
| `/api/delete-account/?token=...` | GET | Public | Delete account via signed URL |

### Profiles
| Endpoint | Method | Permission | Description |
|----------|--------|-----------|-------------|
| `/api/profiles/<username>/` | GET, PATCH | Authenticated + DynamicPagePermission | Get/update user profile |
| `/api/followers/<username>/` | GET, DELETE | Authenticated + DynamicPagePermission | List or remove followers |
| `/api/following/<username>/` | GET, DELETE | Authenticated + DynamicPagePermission | List or unfollow users |

### Social Actions
| Endpoint | Method | Permission | Description |
|----------|--------|-----------|-------------|
| `/api/follow/<username>/` | POST, DELETE | Authenticated | Follow/unfollow or cancel follow request |
| `/api/follow-request/<request_id>/` | POST, DELETE | Authenticated | Accept/reject follow request |
| `/api/block/<user_id>/` | POST, DELETE | Authenticated | Block/unblock a user |
| `/api/mute/<user_id>/` | POST, DELETE | Authenticated | Mute/unmute a user |
| `/api/close-friend/<user_id>/` | POST, DELETE | Authenticated | Add/remove close friends |
| `/api/settings/` | GET, PATCH | Authenticated | Retrieve/update user settings |
| `/api/assign-permission/` | POST | Admin only | Assign page permissions to users |

---

## Pagination
- All list endpoints (followers/following) use `DefaultPagination`.
- Search query supported via `?search=<term>`.

---

## Notes
- All non-public endpoints require authentication.
- Privacy and visibility are enforced at the view-level using `DynamicPagePermission`.
- RBAC allows admins to enable/disable features per URL without code changes.
- Blocking and muting are supported at a granular level for posts and stories.

---

## Setup & Installation

1. Clone the repository.
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Apply migrations:
```bash
python manage.py migrate
```
4. Create a superuser:
```bash
python manage.py createsuperuser
```
5. Run the server:
```bash
python manage.py runserver
```
## License

- This project is open-source and available for personal or commercial use.
