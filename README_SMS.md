DEPRECATED: OTP & Twilio notes

OTP-based registration and debug endpoints have been removed from this repository. The remaining instructions are retained for reference only.

Twilio & OTP Setup (reference)

This project previously supported sending OTPs via SMS (Twilio) and email (SMTP).

1) Twilio setup (recommended for SMS delivery)
- Create a Twilio account and get your `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, and a verified `TWILIO_FROM` phone number.
- Set these as environment variables (Windows PowerShell example):

  $env:TWILIO_ACCOUNT_SID='ACxxxx'
  $env:TWILIO_AUTH_TOKEN='your_token'
  $env:TWILIO_FROM='+1234567890'

2) SMTP setup (email fallback)
- Provide `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS` as environment variables.

3) Development OTP debugging
-- Note: `/debug/otp` and related endpoints have been removed.

4) Loading env vars from a file (optional)
- Install `python-dotenv` and create a `.env` from `.env.example`.

  pip install python-dotenv
  cp .env.example .env

- Then load the variables when running the app (example using `python-dotenv` in a run script) or set them in your system.

5) Notes
- Mobile numbers are expected in international format (e.g. `+1234567890`). Basic client-side validation is included in the register/login pages.
- If Twilio is not configured, OTPs are logged to the application logs as a fallback.
