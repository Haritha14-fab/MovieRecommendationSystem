# TODO - Fix project errors

## Step 1 — Harden dotenv loading (and remove noisy warnings)
- Update `config.py` to load `.env` safely (ignore parsing errors) and optionally only warn.

## Step 2 — Fix registration form mismatch
- Update `routes/auth.py` to read `confirm_password` from POST.
- Validate `password == confirm_password` and return the register template with an error message if not.

✅ Done.

## Step 3 — Re-run basic checks

- Start app (`python app.py`) and confirm there are no runtime exceptions during startup.
- Re-run `python -m py_compile ...`.

## Step 4 — Optional: ensure tests can run
- Install test dependencies if needed (pytest), or run unittest properly.

