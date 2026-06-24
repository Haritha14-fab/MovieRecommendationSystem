Quickstart

1) Create a virtual environment and install dependencies:

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# Unix
source .venv/bin/activate
pip install -r requirements.txt
```

2) Copy `.env.example` to `.env` and set your credentials (FLASK_SECRET). If you need SMTP/Twilio for other integrations, set those as well.

3) Start the dev server:

```bash
python app.py
```

4) Open `http://127.0.0.1:5000` in your browser.

Notes
Note: OTP endpoints were removed; ignore `ALLOW_BULK_OTP` and `DEBUG_OTP` settings.
