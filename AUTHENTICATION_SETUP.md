# 🔐 Authentication & Security Setup Guide

This document outlines the authentication procedures and security measures implemented in the VTT Campaign Dashboard.

## ✅ Authentication Features Implemented

### 1. **Login System** (`/login/`)
- Custom styled login page matching the campaign theme
- Username and password authentication
- Error handling with user-friendly messages
- Auto-redirect to dashboard after successful login
- "Forgot password" link for account recovery

### 2. **Logout System** (`/logout/`)
- Secure logout functionality
- Automatic redirect to login page
- Session cleanup

### 3. **Password Reset Flow**
Complete password reset functionality via email:
- **Step 1**: `/password-reset/` - User enters email address
- **Step 2**: `/password-reset/done/` - Confirmation message displayed
- **Step 3**: Email sent with reset link (valid for 24 hours)
- **Step 4**: `/password-reset-confirm/<token>/` - User sets new password
- **Step 5**: `/password-reset-complete/` - Success confirmation

### 4. **Password Change** (Logged-in users)
- `/password-change/` - Users can update their password
- Requires current password verification
- `/password-change/done/` - Success confirmation

## 🛡️ Security Measures

### Authentication Protection
- All dashboard views require login (`@login_required` decorator)
- Unauthorized users are automatically redirected to login page
- DM-only actions verify `user.is_superuser` before execution

### Password Security
- Minimum 8 characters required
- Cannot be entirely numeric
- Cannot be too similar to username
- Cannot be a commonly used password
- Django's built-in password validators enabled

### Session Security
- **Session timeout**: 24 hours
- **HTTP-only cookies**: Prevents JavaScript access to session cookies
- **SameSite protection**: Mitigates CSRF attacks
- **Secure cookies**: In production, cookies only sent over HTTPS

### CSRF Protection
- All forms include CSRF tokens
- CSRF cookies are HTTP-only and secure in production
- SameSite cookie policy enabled

### Production Security Headers
When `DEBUG=False`, the following security headers are enabled:
- `SECURE_SSL_REDIRECT`: Forces HTTPS
- `HSTS`: HTTP Strict Transport Security (1 year)
- `X-Content-Type-Options`: Prevents MIME sniffing
- `X-Frame-Options`: Prevents clickjacking
- `X-XSS-Protection`: Browser XSS filter

## 📧 Email Configuration

### Development Environment
Emails are printed to the console for testing:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### Production Environment
Configure SMTP settings in your `.env` file:

```env
# Email Settings (for password reset functionality)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@vttcampaign.com
```

#### Gmail Setup Instructions
1. Enable 2-Factor Authentication on your Google account
2. Generate an "App Password" at: https://myaccount.google.com/apppasswords
3. Use the generated app password (not your regular Gmail password)
4. Add credentials to `.env` file

#### Other SMTP Providers
- **SendGrid**: `EMAIL_HOST=smtp.sendgrid.net`, Port 587
- **Mailgun**: `EMAIL_HOST=smtp.mailgun.org`, Port 587
- **AWS SES**: `EMAIL_HOST=email-smtp.us-east-1.amazonaws.com`, Port 587

## 👥 User Management

### DM (Superuser) Accounts
Create via Django management command:
```bash
python manage.py createsuperuser
```

### Player Accounts
DMs can create player accounts through two methods:

1. **Dashboard Interface** (Recommended)
   - DMs have a "Register Sub-User" panel on the dashboard
   - Provides username and password fields
   - Creates standard user accounts (non-superuser)

2. **Django Admin Panel**
   - Access at `/admin/`
   - Full control over user management
   - Can set emails, permissions, and character names

### Character Display Names
- Edit user's "First Name" field in Django admin
- If set, this displays as the character name instead of username
- Example: Username `player1` → First Name `Thorin Oakenshield`
- Shows as "Thorin Oakenshield" in the action feed

## 🔑 Settings Reference

### Core Authentication Settings (`core/settings.py`)

```python
# Redirect URLs
LOGIN_URL = 'login'              # Where to send unauthenticated users
LOGIN_REDIRECT_URL = '/'         # Where to send users after login

# Password Reset
PASSWORD_RESET_TIMEOUT = 86400   # Link valid for 24 hours (in seconds)

# Session Configuration
SESSION_COOKIE_AGE = 86400       # 24 hour session timeout
SESSION_COOKIE_SECURE = True     # Requires HTTPS (production)
SESSION_COOKIE_HTTPONLY = True   # Prevents JavaScript access
SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
```

## 🧪 Testing Authentication

### Test Login Flow
1. Navigate to `http://localhost:8000/`
2. Should redirect to `/login/` if not authenticated
3. Enter valid credentials
4. Should redirect to dashboard

### Test Password Reset (Development)
1. Go to `/login/`
2. Click "Forgot your password?"
3. Enter any email (even if not configured)
4. Check console for password reset email
5. Copy the reset link from console output
6. Visit the link and set new password

### Test DM Permissions
1. Log in as a regular player
2. Try to access `/review/`
3. Should redirect to dashboard (access denied)
4. DM controls should not be visible

## 🚨 Security Best Practices

### For Development
- ✅ Keep `SECRET_KEY` in `.env` file
- ✅ Never commit `.env` to version control
- ✅ Use strong passwords even in development
- ✅ Test authentication flows regularly

### For Production
- ✅ Set `DEBUG=False` in `.env`
- ✅ Use a strong, random `SECRET_KEY`
- ✅ Configure proper SMTP for emails
- ✅ Use HTTPS (handled by Vercel automatically)
- ✅ Regularly update dependencies
- ✅ Monitor for suspicious login attempts
- ✅ Keep Django and packages up to date

### Password Requirements Enforcement
Django's password validators are configured in `settings.py`:
```python
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

## 📱 Mobile Compatibility

All authentication pages are fully responsive:
- Mobile-friendly login/password reset forms
- Touch-optimized buttons
- Readable on small screens
- Consistent theming across devices

## 🎨 Customization

All authentication templates are located in:
```
game/templates/registration/
├── login.html                      # Login page
├── password_reset_form.html        # Request password reset
├── password_reset_done.html        # Email sent confirmation
├── password_reset_confirm.html     # Set new password
├── password_reset_complete.html    # Reset successful
├── password_change_form.html       # Change password (logged in)
└── password_change_done.html       # Change successful
```

Templates use inline CSS matching your campaign theme:
- Dark fantasy color scheme
- Gold (#ffaa00) accent colors
- Smooth animations
- Consistent with main dashboard styling

## 🔍 Troubleshooting

### "CSRF verification failed"
- Ensure `{% csrf_token %}` is in all forms
- Check that `django.middleware.csrf.CsrfViewMiddleware` is in `MIDDLEWARE`
- Clear browser cookies and try again

### Password reset emails not sending
- In development: Check console output
- In production: Verify SMTP credentials in `.env`
- Check email spam folder
- Ensure `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` are correct

### "Permission denied" errors
- Verify user has appropriate permissions
- Check `@login_required` decorators are in place
- Ensure DM actions check `user.is_superuser`

### Session expires too quickly
- Adjust `SESSION_COOKIE_AGE` in settings (default 24 hours)
- Consider "Remember me" functionality if needed

## 📚 Additional Resources

- [Django Authentication Documentation](https://docs.djangoproject.com/en/stable/topics/auth/)
- [Django Security Best Practices](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Security Guidelines](https://owasp.org/www-project-top-ten/)

## ✨ Summary

Your VTT Campaign Dashboard now has a complete, secure authentication system including:

✅ Login/Logout functionality  
✅ Password reset via email  
✅ Password change for logged-in users  
✅ CSRF protection  
✅ Session security  
✅ DM permission controls  
✅ Mobile-responsive templates  
✅ Production-ready security headers  
✅ Comprehensive error handling  

All authentication flows are fully functional and ready for production use!
