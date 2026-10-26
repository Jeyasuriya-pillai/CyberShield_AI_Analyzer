import html
import re
from urllib.parse import urlparse

import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CyberShield AI Security Analyzer",
    page_icon="🛡️",
    layout="centered",
)

# ============================================================
# CUSTOM CSS
# ============================================================

THEMES = {
    "Terminal": {
        "bg": "#030806", "bgimg": "repeating-linear-gradient(0deg,rgba(255,255,255,.02) 0 1px,transparent 1px 4px)",
        "panel": "#07110c", "text": "#c8ffe6", "muted": "#6fa890", "line": "#14502f",
        "accent": "#00ff9c", "accent_text": "#00160d", "accent2": "#22d3ee",
        "good": "#00ff9c", "warn": "#ffd60a", "bad": "#ff4d6d",
        "font": "'JetBrains Mono'", "radius": "4px", "bw": "1px",
        "shadow": "none", "btn_shadow": "0 0 22px rgba(0,255,156,.35)",
        "bar": "#0a1a12", "bar_text": "#6fa890",
    },
    "Neo Light": {
        "bg": "#fff6e0", "bgimg": "radial-gradient(rgba(17,17,17,.14) 1px,transparent 1px) 0 0/18px 18px",
        "panel": "#ffffff", "text": "#111111", "muted": "#555555", "line": "#111111",
        "accent": "#ffd60a", "accent_text": "#111111", "accent2": "#ff5ea8",
        "good": "#15803d", "warn": "#b45309", "bad": "#e11d48",
        "font": "'Space Grotesk'", "radius": "10px", "bw": "2px",
        "shadow": "6px 6px 0 #111111", "btn_shadow": "4px 4px 0 #111111",
        "bar": "#ffd60a", "bar_text": "#111111",
    },
}

theme_name = st.session_state.get("theme", "Terminal")
if theme_name not in THEMES:
    theme_name = "Terminal"

ROOT_VARS = ":root{" + "".join(f"--{k}:{v};" for k, v in THEMES[theme_name].items()) + "}"

STATIC_CSS = """
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Space+Grotesk:wght@500;700&display=swap');

#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"]{display:none !important;}
header[data-testid="stHeader"]{background:transparent;}
.stApp{background:var(--bgimg),var(--bg);color:var(--text);font-family:var(--font),monospace;}
.block-container{max-width:1060px;padding-top:1rem;padding-bottom:3rem;}
.stApp [data-testid="stMarkdownContainer"]{color:var(--text);font-family:var(--font),monospace;}
[data-testid="stHeading"], [data-testid="stHeading"] *, [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] *,
[data-testid="stRadio"] label, [data-testid="stRadio"] label *, [data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] *{color:var(--text) !important;font-family:var(--font),monospace !important;}
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] *{color:var(--muted) !important;}
hr{border-color:var(--line) !important;}

/* top bar */
.topbar{display:flex;align-items:center;margin:6px 0 18px;}
.brand{font-weight:800;font-size:18px;letter-spacing:1px;color:var(--text);}
.brand b{color:var(--accent);}
.online{margin-left:auto;font-size:12px;font-weight:700;letter-spacing:1px;color:var(--good);}
.online i{display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--good);margin-right:8px;
  animation:pulse 1.6s infinite;}
@keyframes pulse{50%{opacity:.25;}}

/* hero window */
.win{border:var(--bw) solid var(--line);border-radius:var(--radius);background:var(--panel);box-shadow:var(--shadow);overflow:hidden;}
.win-bar{display:flex;align-items:center;gap:8px;padding:11px 16px;background:var(--bar);border-bottom:var(--bw) solid var(--line);}
.d{width:12px;height:12px;border-radius:50%;border:1px solid rgba(0,0,0,.45);display:inline-block;}
.d1{background:#ff5f56;} .d2{background:#ffbd2e;} .d3{background:#27c93f;}
.win-title{margin-left:10px;font-size:12px;color:var(--bar_text);}
.win-body{padding:44px 48px 46px;}
.prompt{font-size:14px;color:var(--accent2);margin-bottom:20px;}
.prompt .cur{display:inline-block;animation:blink 1s steps(2) infinite;}
@keyframes blink{50%{opacity:0;}}
.h{font-weight:800;font-size:clamp(34px,5vw,60px);line-height:1.08;letter-spacing:-1.5px;color:var(--text);margin-bottom:20px;}
.mark{background:var(--accent);color:var(--accent_text);padding:0 .18em;}
.txt{max-width:560px;color:var(--muted);font-size:15px;line-height:1.75;margin-bottom:26px;}
.chips{display:flex;flex-wrap:wrap;gap:10px;}
.chips span{padding:7px 14px;border:var(--bw) solid var(--line);border-radius:var(--radius);font-size:12px;
  font-weight:700;color:var(--text);background:transparent;}
.chips span::before{content:"> ";color:var(--accent2);}

/* module cards */
.mods{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin:22px 0 28px;}
.mod{padding:22px;border:var(--bw) solid var(--line);border-radius:var(--radius);background:var(--panel);box-shadow:var(--shadow);}
.mod small{display:block;color:var(--accent2);font-size:11px;font-weight:700;letter-spacing:1.4px;margin-bottom:12px;}
.mod b{display:block;font-size:17px;margin-bottom:8px;color:var(--text);}
.mod span{display:block;color:var(--muted);font-size:13px;line-height:1.6;}

/* tabs */
div[data-baseweb="tab-list"]{gap:8px;padding:0;background:transparent;border:0;}
button[data-baseweb="tab"]{flex:1;height:48px;border:var(--bw) solid var(--line);border-radius:var(--radius);
  background:var(--panel);color:var(--text);font-weight:700;}
button[data-baseweb="tab"] p{color:inherit !important;font-family:var(--font),monospace !important;font-weight:700;}
button[data-baseweb="tab"][aria-selected="true"]{background:var(--accent);color:var(--accent_text);box-shadow:var(--btn_shadow);}
div[data-baseweb="tab-highlight"],div[data-baseweb="tab-border"]{display:none !important;}
div[data-baseweb="tab-panel"]{margin-top:16px;padding:28px !important;border:var(--bw) solid var(--line);
  border-radius:var(--radius);background:var(--panel);box-shadow:var(--shadow);}

/* inputs */
.stTextInput div[data-baseweb="input"],.stTextArea div[data-baseweb="textarea"]{
  background:var(--bg) !important;border:var(--bw) solid var(--line) !important;border-radius:var(--radius) !important;}
.stTextInput div[data-baseweb="input"]:focus-within,.stTextArea div[data-baseweb="textarea"]:focus-within{
  border-color:var(--accent) !important;box-shadow:0 0 0 2px var(--accent);}
.stTextInput input,.stTextArea textarea{background:transparent !important;color:var(--text) !important;
  -webkit-text-fill-color:var(--text) !important;border:0 !important;font-family:var(--font),monospace !important;}
.stTextInput input::placeholder,.stTextArea textarea::placeholder{color:var(--muted) !important;
  -webkit-text-fill-color:var(--muted) !important;}

/* button */
.stButton > button{height:50px;border:var(--bw) solid var(--line);border-radius:var(--radius);font-weight:800;
  background:var(--accent);color:var(--accent_text);box-shadow:var(--btn_shadow);transition:transform .08s;}
.stButton > button p{color:var(--accent_text) !important;font-family:var(--font),monospace !important;font-weight:800;}
.stButton > button:hover{border-color:var(--line);color:var(--accent_text);transform:translate(-2px,-2px);}
.stButton > button:active{transform:translate(2px,2px);box-shadow:none;}

/* results */
.result{margin-top:18px;padding:22px;border:var(--bw) solid;border-radius:var(--radius);box-shadow:var(--shadow);}
.result .label{font-size:11px;letter-spacing:1.5px;color:var(--muted);}
.score{font-size:52px;font-weight:800;line-height:1.1;}
.verdict{font-size:24px;font-weight:800;margin:2px 0 4px;}
.safe{background:color-mix(in srgb,var(--good) 12%,var(--panel));border-color:var(--good);}
.safe .verdict,.safe .score{color:var(--good);}
.suspicious{background:color-mix(in srgb,var(--warn) 12%,var(--panel));border-color:var(--warn);}
.suspicious .verdict,.suspicious .score{color:var(--warn);}
.dangerous{background:color-mix(in srgb,var(--bad) 12%,var(--panel));border-color:var(--bad);}
.dangerous .verdict,.dangerous .score{color:var(--bad);}
.signal{background:var(--bg);border:var(--bw) solid var(--line);border-left:5px solid var(--accent2);
  padding:11px 15px;margin:8px 0;border-radius:var(--radius);font-size:13px;color:var(--text);}

@media(max-width:850px){
  .win-body{padding:28px 22px;}
  .mods{grid-template-columns:1fr;}
}
"""

st.markdown("<style>" + ROOT_VARS + STATIC_CSS + "</style>", unsafe_allow_html=True)


# ============================================================
# HELPERS
# ============================================================

def find_terms(text, terms):
    """Match whole words/phrases only (so 'now' does not match 'know')."""
    return [t for t in terms if re.search(r"\b" + re.escape(t) + r"\b", text)]


# ============================================================
# PASSWORD ANALYZER
# ============================================================

def analyze_password(password):
    score = 0
    signals = []
    recommendations = []

    length = len(password)

    if length >= 16:
        score += 30
        signals.append("Excellent password length.")
    elif length >= 12:
        score += 24
        signals.append("Good password length.")
    elif length >= 8:
        score += 15
        signals.append("Password length is acceptable, but 12+ is recommended.")
        recommendations.append("Increase the password to at least 12 characters.")
    else:
        signals.append("Password is too short.")
        recommendations.append("Use at least 12 characters.")

    if re.search(r"[A-Z]", password):
        score += 12
    else:
        recommendations.append("Add uppercase letters.")

    if re.search(r"[a-z]", password):
        score += 12
    else:
        recommendations.append("Add lowercase letters.")

    if re.search(r"\d", password):
        score += 12
    else:
        recommendations.append("Add numbers.")

    if re.search(r"[^A-Za-z0-9]", password):
        score += 15
    else:
        recommendations.append("Add special characters.")

    if re.search(r"(.)\1\1", password):
        score -= 15
        signals.append("Repeated characters detected.")
        recommendations.append("Avoid repeated characters such as aaa or 111.")

    lower = password.lower()

    for seq in ["123456", "234567", "345678", "abcdef", "qwerty", "asdfgh", "password"]:
        if seq in lower:
            score -= 25
            signals.append("Common sequence detected.")
            recommendations.append("Avoid sequences such as 123456, qwerty or password.")
            break

    common = {
        "password", "123456", "12345678", "qwerty", "admin", "letmein",
        "welcome", "iloveyou", "password123", "admin123",
    }

    if lower in common:
        score = 5
        signals.append("This is a commonly used password.")
        recommendations.append("Use a completely unique password.")

    # Standalone year only (1900-2099), not part of a longer number
    if re.search(r"(?<!\d)(19|20)\d{2}(?!\d)", password):
        score -= 5
        signals.append("A year-like pattern was detected.")
        recommendations.append("Avoid using years or birth dates.")

    score = max(0, min(100, score))

    if score >= 75:
        verdict, title, css = "SAFE", "Strong Password", "safe"
    elif score >= 45:
        verdict, title, css = "SUSPICIOUS", "Moderate Password", "suspicious"
    else:
        verdict, title, css = "DANGEROUS", "Weak Password", "dangerous"

    if not recommendations:
        recommendations.append("Keep this password unique and never reuse it.")

    return score, verdict, title, signals, list(dict.fromkeys(recommendations)), css


# ============================================================
# MESSAGE ANALYZER
# ============================================================

def analyze_message(message):
    text = message.lower()

    score = 0
    signals = []
    recommendations = []

    phishing_words = [
        "verify your account", "verify account", "click here", "confirm your account",
        "account suspended", "account blocked", "login immediately", "security alert",
        "unusual activity",
    ]
    urgency_words = [
        "urgent", "immediately", "act now", "right now", "within 24 hours",
        "limited time", "final warning",
    ]
    credential_words = [
        "password", "otp", "one time password", "verification code",
        "login", "username", "pin", "cvv",
    ]
    financial_words = [
        "bank", "credit card", "debit card", "payment", "refund", "money",
        "upi", "transaction", "wallet",
    ]
    threat_words = [
        "suspended", "blocked", "legal action", "police", "penalty", "fine",
    ]

    if find_terms(text, phishing_words):
        score += 25
        signals.append("Phishing-style language detected.")

    if find_terms(text, urgency_words):
        score += 15
        signals.append("Urgency or pressure detected.")

    if find_terms(text, credential_words):
        score += 20
        signals.append("Message requests or mentions sensitive credentials.")

    if find_terms(text, financial_words):
        score += 15
        signals.append("Financial/payment-related language detected.")

    if find_terms(text, threat_words):
        score += 15
        signals.append("Threatening or account-lock language detected.")

    urls = re.findall(r"https?://\S+|www\.\S+", text)

    if urls:
        score += 15
        signals.append("URL/link detected in the message.")

    if (
        find_terms(text, ["password", "otp"])
        and (find_terms(text, ["click", "link"]) or urls)
    ):
        score += 15
        signals.append("Credential request combined with a link.")

    score = max(0, min(100, score))

    if score >= 60:
        verdict, title, css = "DANGEROUS", "Likely Phishing / Scam", "dangerous"
    elif score >= 30:
        verdict, title, css = "SUSPICIOUS", "Suspicious Message", "suspicious"
    else:
        verdict, title, css = "SAFE", "No Major Red Flags", "safe"

    recommendations.append(
        "Do not share passwords, OTPs or banking details through suspicious messages."
    )

    if urls:
        recommendations.append("Verify links carefully before opening them.")

    if score < 30:
        recommendations.append(
            "Static analysis cannot guarantee that a message is legitimate."
        )

    return score, verdict, title, signals, recommendations, css


# ============================================================
# URL ANALYZER
# ============================================================

def analyze_url(url):
    score = 0
    signals = []
    recommendations = []

    original = url.strip()

    invalid = (
        0, "DANGEROUS", "Invalid URL",
        ["The text could not be parsed as a valid website URL."],
        ["Enter a valid URL such as https://example.com."],
        "dangerous",
    )

    if not original:
        return invalid

    if re.match(r"^https?://", original, re.I):
        url_to_parse = original
    else:
        url_to_parse = "http://" + original

    try:
        parsed = urlparse(url_to_parse)
        host = (parsed.hostname or "").lower()
    except ValueError:
        return invalid

    if not host:
        return invalid

    full_lower = original.lower()

    # HTTPS
    if full_lower.startswith("https://"):
        signals.append("HTTPS is enabled.")
    else:
        score += 20
        signals.append("HTTPS is not used.")
        recommendations.append("Prefer HTTPS websites.")

    # IP address
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host):
        score += 30
        signals.append("URL uses a raw IP address instead of a domain.")

    # @ symbol
    if "@" in original:
        score += 30
        signals.append("URL contains '@', which can hide the real destination.")

    # Punycode
    if "xn--" in host:
        score += 25
        signals.append("Punycode domain detected.")

    # Shorteners (exact domain or subdomain of it)
    shorteners = [
        "bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "ow.ly", "buff.ly",
        "cutt.ly", "shorturl.at", "rebrand.ly", "tiny.cc",
    ]

    if any(host == s or host.endswith("." + s) for s in shorteners):
        score += 20
        signals.append("URL shortener detected.")
        recommendations.append("Verify the final destination of shortened links.")

    # Suspicious TLDs
    suspicious_tlds = [
        ".tk", ".ml", ".ga", ".cf", ".gq", ".click", ".top", ".xyz",
        ".zip", ".mov", ".work", ".download",
    ]

    if any(host.endswith(tld) for tld in suspicious_tlds):
        score += 15
        signals.append("Higher-risk/suspicious TLD detected.")

    # Too many subdomains
    if host.count(".") >= 4:
        score += 15
        signals.append("Unusually high number of subdomains.")
        recommendations.append("Check the actual registered domain.")

    # Long URL
    if len(original) > 120:
        score += 10
        signals.append("Unusually long URL.")

    # Suspicious words
    suspicious_words = [
        "login", "verify", "verification", "secure", "account", "update",
        "password", "wallet", "payment", "free", "claim", "bonus", "gift", "confirm",
    ]

    matches = [w for w in suspicious_words if w in full_lower]

    if len(matches) >= 2:
        score += 15
        signals.append("Multiple suspicious URL keywords detected.")
        recommendations.append("Verify that the domain is the official website.")

    # Encoded characters
    if re.search(r"%[0-9a-f]{2}", original, re.I):
        score += 5
        signals.append("Encoded URL characters detected.")

    # Many hyphens
    if host.count("-") >= 3:
        score += 10
        signals.append("Domain contains many hyphens.")

    score = max(0, min(100, score))

    if score >= 55:
        verdict, title, css = "DANGEROUS", "High-Risk URL", "dangerous"
    elif score >= 25:
        verdict, title, css = "SUSPICIOUS", "Suspicious URL", "suspicious"
    else:
        verdict, title, css = "SAFE", "No Major URL Red Flags", "safe"

    recommendations.append("Check the domain name carefully before entering credentials.")
    recommendations.append(
        "Static URL analysis cannot guarantee that a website is legitimate."
    )

    return score, verdict, title, signals, list(dict.fromkeys(recommendations)), css


# ============================================================
# RESULT DISPLAY
# ============================================================

def show_result(result):
    score, verdict, title, signals, recommendations, css = result

    st.markdown(
        f"""
        <div class="result {css}">
            <div class="label">SECURITY VERDICT</div>
            <div class="score">{int(score)}/100</div>
            <div class="verdict">{html.escape(verdict)}</div>
            <div style="color:#b8c0c8;">{html.escape(title)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### 🔎 Security Signals")

    if signals:
        for s in signals:
            st.markdown(
                f'<div class="signal">⚠️ {html.escape(s)}</div>',
                unsafe_allow_html=True,
            )
    else:
        st.success("No major suspicious indicators were detected.")

    st.markdown("#### 🛡️ Recommendations")

    for r in recommendations:
        st.markdown(f"- {r}")


# ============================================================
# HEADER
# ============================================================

_, theme_col = st.columns([3, 2])
theme_col.radio("Theme", list(THEMES.keys()), horizontal=True, key="theme", label_visibility="collapsed")

st.markdown("""
<div class="topbar">
<div class="brand">[ CYBER<b>SHIELD</b> ]</div>
<div class="online"><i></i>SYSTEM ONLINE</div>
</div>
<div class="win">
<div class="win-bar"><span class="d d1"></span><span class="d d2"></span><span class="d d3"></span>
<span class="win-title">cybershield@analyzer: ~/scan</span></div>
<div class="win-body">
<div class="prompt">$ ./cybershield --analyze<span class="cur"> ▍</span></div>
<div class="h">Think before<br>you <span class="mark">click.</span></div>
<div class="txt">Scan passwords, suspicious messages and links with rule-based detection. Get a 0-100 risk score, the exact warning signs and what to do next.</div>
<div class="chips"><span>passwords</span><span>messages</span><span>urls</span></div>
</div>
</div>
<div class="mods">
<div class="mod"><small>MODULE 01</small><b>Password Strength</b><span>Length, character variety, common passwords and predictable patterns.</span></div>
<div class="mod"><small>MODULE 02</small><b>Phishing Detection</b><span>Urgency, credential requests, financial lures and threatening language.</span></div>
<div class="mod"><small>MODULE 03</small><b>URL Inspection</b><span>HTTPS, raw IPs, shorteners, punycode, risky endings and keywords.</span></div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3 = st.tabs([
    "🔐 Password Analyzer",
    "💬 Message Analyzer",
    "🔗 URL Analyzer",
])

with tab1:
    st.subheader("Password Security Analysis")

    password = st.text_input(
        "Enter a password to analyze",
        type="password",
        placeholder="Enter password...",
    )

    if st.button("🔍 Analyze Password", key="password_btn", use_container_width=True):
        if not password:
            st.warning("Please enter a password.")
        else:
            show_result(analyze_password(password))

with tab2:
    st.subheader("Phishing & Scam Message Analysis")

    message = st.text_area(
        "Paste the message here",
        height=220,
        max_chars=5000,
        placeholder="Example: Your account has been suspended. Click here to verify...",
    )

    st.caption(f"Characters: {len(message)} / 5000")

    if st.button("🔍 Analyze Message", key="message_btn", use_container_width=True):
        if not message.strip():
            st.warning("Please enter a message.")
        else:
            show_result(analyze_message(message))

with tab3:
    st.subheader("Website / URL Security Analysis")

    url = st.text_input("Enter a URL", placeholder="https://example.com")

    if st.button("🔍 Analyze URL", key="url_btn", use_container_width=True):
        if not url.strip():
            st.warning("Please enter a URL.")
        else:
            show_result(analyze_url(url))

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "CyberShield uses rule-based static analysis. "
    "Results are indicators, not a 100% guarantee of safety."
)