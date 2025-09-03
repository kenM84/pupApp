# Authentication System - RUSH PUP!

This document describes the authentication system implemented for the RUSH PUP! adult website.

## Features

- **User Registration**: Users can create accounts with username, email, and password
- **User Login**: Secure authentication with password hashing
- **Session Management**: Persistent sessions using Flask-Session
- **Protected Routes**: All main routes require authentication
- **Password Security**: Passwords are hashed using Werkzeug's security functions
- **Database Integration**: User data stored in Azure SQL Database using pymssql driver

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database

Run the database initialization script:

```bash
python init_db.py
```

This will:
- Create the database tables
- Optionally create an admin user for testing

### 3. Environment Variables

Set the following environment variables:

```bash
# Required for production
export SECRET_KEY="your-secret-key-here"

# Database connection (optional - defaults to SQLite)
export DATABASE_URL="your-azure-sql-connection-string"
```

### 4. Run the Application

```bash
python app.py
```

## Authentication Flow

1. **Unauthenticated Access**: Users trying to access protected routes are redirected to `/login`
2. **Login Process**: Users enter credentials on the login page
3. **Session Creation**: Upon successful authentication, a session is created
4. **Redirect**: Users are redirected to their originally requested page or the home page
5. **Authenticated Access**: Users can access all protected content
6. **Logout**: Users can logout, which destroys their session

## Routes

- `/` - Home page (protected)
- `/login` - Login page
- `/register` - Registration page
- `/logout` - Logout (protected)
- `/greyscale_demo` - Demo page (protected)

## Database Schema

The `users` table includes:
- `id` - Primary key
- `username` - Unique username
- `email` - Unique email address
- `password_hash` - Hashed password
- `salt` - Password salt (for additional security)
- `is_active` - Account status
- `created_at` - Account creation timestamp
- `last_login` - Last login timestamp

## Security Features

- **Password Hashing**: Uses Werkzeug's secure password hashing
- **Session Security**: Sessions are signed and stored securely
- **CSRF Protection**: Built-in CSRF protection via Flask-Session
- **Input Validation**: Form validation for all user inputs
- **SQL Injection Protection**: Uses SQLAlchemy ORM for safe database queries

## Development Notes

- Default admin user: `admin` / `admin123` (change in production!)
- Session files stored in `./flask_session/` directory
- Uses pymssql driver for Azure SQL Database (no ODBC driver required)
- All routes except login/register require authentication

## Production Considerations

1. **Change Default Secret Key**: Set a strong `SECRET_KEY` environment variable
2. **Azure SQL Configuration**: Ensure KeyVault contains `sqlDBServer`, `sqlDBName`, `appDBUname`, and `AppDBPassword`
3. **HTTPS**: Ensure all authentication happens over HTTPS
4. **Session Storage**: Consider using Redis or database sessions for production
5. **Password Policy**: Implement stronger password requirements
6. **Rate Limiting**: Add rate limiting for login attempts
7. **Email Verification**: Add email verification for new accounts
