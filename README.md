# CyberShield — AI Security Analyzer

## Project structure

```text
CyberShield/
├── index.html
├── style.css
├── script.js
├── config.php
└── api/
    └── analyze.php
```

## Features
- AI password strength analysis
- AI phishing/scam message analysis
- AI suspicious URL analysis
- Password itself is NOT sent to AI; only derived security features are sent
- Session-only recent scan history
- Responsive dark cybersecurity UI

## XAMPP setup

1. Copy the `CyberShield` folder to:
   `C:\xampp\htdocs\CyberShield`
2. Open `config.php`.
3. Put your Gemini API key in `api_key`.
4. Start Apache in XAMPP.
5. Open:
   `http://localhost/CyberShield/`

## Important
- Do not upload `config.php` containing a real API key to GitHub.
- The backend uses PHP cURL to call Gemini.
- If your Gemini account uses a different available model, change the `model` value in `config.php`.
