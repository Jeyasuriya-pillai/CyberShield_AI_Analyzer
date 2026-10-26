# 🛡️ CyberShield — AI Security Analyzer

### A Web-Based Security Analyzer for Passwords, Messages, and URLs

CyberShield is a web-based security application designed to identify potentially weak passwords, suspicious messages, and risky URLs. It helps users recognize common online security threats through automated analysis.

---

## 🌐 Live Demo

🚀 **Try CyberShield Online**

https://cybershield-ai-analyzer.streamlit.app/

---

## ✨ Features

- 🔐 Password Analyzer
- 💬 Message Analyzer
- 🔗 URL Analyzer
- 🚨 Phishing Keyword Detection
- 🔎 Suspicious Pattern Detection
- 🛡️ Security Awareness
- 🖥️ Web-Based Interface
- ☁️ Streamlit Cloud Deployment

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Web application interface |
| PHP | Analyzer components |
| HTML | Web page structure |
| CSS | Styling and UI |
| JavaScript | Interactive functionality |
| Git & GitHub | Version control and hosting |
| Streamlit Community Cloud | Application deployment |

---

## 🧠 How It Works

    User Input
         |
         v
    Select Analyzer
         |
    +----+----+
    |    |    |
    v    v    v
 Password Message URL
 Analyzer Analyzer Analyzer
    |    |    |
    +----+----+
         |
         v
    Security Checks
         |
         v
    Analyze Results
         |
         v
    Display Findings

CyberShield analyzes user input using the checks implemented in the selected analyzer and displays potential security warning signs.

---

## 📁 Project Structure

    CyberShield_AI_Analyzer/
    |
    ├── .streamlit/
    │   └── config.toml
    |
    ├── analyzer/
    │   ├── index.php
    │   ├── message_analyzer.php
    │   ├── password_analyzer.php
    │   └── url_analyzer.php
    |
    ├── data/
    │   ├── common_passwords.php
    │   ├── phishing_keywords.php
    │   └── suspicious_patterns.php
    |
    ├── analyzer.php
    ├── app.py
    ├── index.php
    ├── requirements.txt
    ├── script.js
    ├── style.css
    └── README.md

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

    git clone https://github.com/Jeyasuriya-pillai/CyberShield_AI_Analyzer.git

### 2. Navigate to the Project

    cd CyberShield_AI_Analyzer

### 3. Create a Virtual Environment

    python -m venv venv

### 4. Activate the Environment

**Windows:**

    venv\Scripts\activate

### 5. Install Dependencies

    pip install -r requirements.txt

### 6. Run the Application

    python -m streamlit run app.py

Open the local URL displayed in your terminal, usually:

    http://localhost:8501

---

## 🧪 Example Phishing Message

Use this fictional message to test the message analyzer.

    URGENT: Your bank account will be blocked today!

    Verify your account immediately to avoid permanent suspension.

    Click here:
    http://example.com/verify-account

    You have only 30 minutes remaining!

### Potential Warning Signs

- Urgent language
- Account suspension threats
- Suspicious verification link
- Pressure to act immediately

---

## 🔒 Security Disclaimer

- Do not enter real passwords or confidential information into a public testing application.
- Never share OTPs or banking credentials through suspicious links.
- Verify suspicious messages through official communication channels.
- A result marked safe does not guarantee that content is trustworthy.
- This project is intended for security awareness and educational purposes.

---

## 🚧 Project Status

**Status: Under Development**

### Core Components

- Password Analyzer
- Message Analyzer
- URL Analyzer
- Common Password Data
- Phishing Keyword Data
- Suspicious Pattern Data
- Streamlit Deployment

### Future Enhancements

- Improved user interface
- Detailed risk analysis
- Enhanced phishing detection
- Security recommendations
- Downloadable analysis reports

---

## 👨‍💻 Developer Information

| Information | Details |
|---|---|
| Developer | Jeyasuriya |
| Course | B.Sc. Information Technology |
| Project | CyberShield — AI Security Analyzer |
| Deployment | Streamlit Community Cloud |

---
