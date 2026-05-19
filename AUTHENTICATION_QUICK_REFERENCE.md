# 🔐 Authentication Quick Reference

## Available URLs

### Public (No Login Required)
- `/login/` - Login page
- `/password-reset/` - Request password reset
- `/password-reset/done/` - Reset email sent confirmation
- `/password-reset-confirm/<uidb64>/<token>/` - Set new password
- `/password-reset-complete/` - Reset complete confirmation

### Authenticated Users
- `/` - Campaign Dashboard (redirects to `/login/` if not authenticated)
- `/logout/` - Logout
- `/password-change/` - Change password
- `/password-change/done/` - Password change success
- `/api/live-feed/` - Real-time feed API
- `/api/active-map/` - Active map API

### DM Only (Superuser)
- `/admin/` - Django admin panel
- `/review/` - DM review panel
- `/review/action/<post_id>/<decision>/` - Approve/reject actions
- `/delete-asset/<asset_id>/` - Delete background asset
- `/delete-post/<post_id>/` - Delete player post
- `/api/pending-queue/` - Pending submissions API

## Quick Commands

### Create Superuser (DM)
```bash
python manage.py createsuperuser
```

### Run Development Server
```bash
python manage.py runserver
```

### Test Login System
1. Start server: `python manage.py runserver`
2. Visit: `http://localhost:8000/`
3. Should redirect to login page
4. Login with credentials

### Test Password Reset (Development)
1. Visit: `http://localhost:8000/login/`
2. Click "Forgot your password?"
3. Enter any email
4. Check **console output** for reset link
5. Copy and visit the link
6. Set new password

## Security Checklist

### ✅ Implemented Features
- [x] Login/Logout functionality
- [x] Password reset via email
- [x] Password change for logged-in users
- [x] CSRF protection on all forms
- [x] Session security (24-hour timeout)
- [x] Secure cookies in production
- [x] DM permission checks
- [x] Password validators
- [x] Production security headers
- [x] Mobile-responsive templates

### 📧 Email Configuration

**Development** (Current):
- Emails print to console
- No SMTP configuration needed

**Production** (Add to `.env`):
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@vttcampaign.com
```

## File Structure

```
game/templates/registration/
├── login.html                      # Login page
├── password_reset_form.html        # Request reset
├── password_reset_done.html        # Email sent
├── password_reset_confirm.html     # New password
├── password_reset_complete.html    # Success
├── password_change_form.html       # Change password
└── password_change_done.html       # Change success
```

## Common Issues & Solutions

### Issue: "CSRF verification failed"
**Solution**: Clear browser cookies or open in incognito mode

### Issue: Password reset email not received
**Solution**: In development, check console output (not actual email)

### Issue: Can't access dashboard
**Solution**: Make sure you're logged in and have proper permissions

### Issue: DM controls not visible
**Solution**: Login as superuser created with `createsuperuser` command

## Next Steps

1. ✅ **Test the login system** - Try accessing the dashboard
2. ✅ **Create test accounts** - Create DM and player accounts
3. ✅ **Test password reset** - Verify email functionality
4. ⚠️ **Configure production email** - When deploying to production
5. ⚠️ **Review security settings** - Before going live

## Support

For detailed information, see:
- `AUTHENTICATION_SETUP.md` - Full setup guide
- `QUICK_START.md` - General quick start
- `FEATURES.md` - Feature documentation
