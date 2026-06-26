---
name: testing-flask-registration
description: Test the Flask registration page end-to-end. Use when verifying registration UI, form validation, or auth flow changes.
---

# Testing Flask Registration Page

## Prerequisites
- Flask app running locally on port 5000
- SQLite database initialized (happens automatically on first run)

## Setup
```bash
cd /home/ubuntu/MovieRecommendationSystem
# Kill any existing process on port 5000
fuser -k 5000/tcp 2>/dev/null
# Start Flask dev server
python run.py &
```

Note: `lsof` might not be available on the VM; use `fuser` or `ss -tlnp` instead to check ports.

## Key Files
- `templates/register.html` - Registration template
- `templates/login.html` - Login template (for verifying redirect)
- `routes/auth.py` - Auth routes (register/login endpoints)
- `static/js/register.js` - Client-side validation (password strength, match check, show/hide toggle)
- `static/css/register.css` - Registration page styles
- `database/user_store.py` - User creation and authentication logic

## Test Plan (7 tests)

### Test 1: All form fields render
Navigate to `/register`. Verify: Name, Email, Mobile, Password (with Show button), Confirm Password, Register button, "Login Here" link all visible.

### Test 2: Password show/hide toggle
Type in Password field, click "Show" button. Verify password becomes visible plaintext and button text changes to "Hide".

### Test 3: Password strength indicator
- Type single char "a" -> expect "Too weak" with red/danger progress bar
- Type strong password like "aB1!xY2@" -> expect "Strong" with green/success progress bar
- The JS element IDs are: `strengthBar`, `strengthText`

### Test 4: Password match/mismatch
- Type different passwords in Password and Confirm Password -> "Passwords do not match" in red
- Type matching passwords -> "Passwords match" in green
- The JS element ID is: `matchMessage`

### Test 5: Successful registration
Fill all fields with unique credentials (use timestamp-based email to avoid duplicates). Click Register. Verify redirect to `/login`.

### Test 6: Duplicate registration
Re-submit the same credentials. Verify "User already exists" error in red alert box, page stays on `/register`.

### Test 7: Login Here link
Click "Login Here" link at bottom of register page. Verify navigation to `/login`.

## Tips
- The form fields expected by the backend are: `username`, `email`, `mobile` (optional), `password`. The confirm password field is `confirm_password` and is only validated client-side.
- The database uses SQLite with a UNIQUE constraint on email, so duplicate detection is based on email address.
- Password validation is client-side only (via `register.js`). There is no server-side password strength enforcement.
- If the database file might have stale test data, you can delete it and restart the app to get a fresh database.
- The `register.js` file uses `document.getElementById()` with specific IDs: `password`, `confirmPassword`, `showPassword`, `strengthBar`, `strengthText`, `matchMessage`.

## Devin Secrets Needed
None - this is a local Flask app with no external services.
