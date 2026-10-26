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

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root{
  --bg:#f5f7fb; --card:#ffffff; --text:#0f172a; --muted:#64748b; --line:#e2e8f0;
  --blue:#2563eb; --blue-d:#1d4ed8; --blue-l:#eff4ff;
  --green:#16a34a; --amber:#d97706; --red:#dc2626;
}
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"]{display:none !important;}
header[data-testid="stHeader"]{background:transparent;}
.stApp{background:var(--bg);color:var(--text);font-family:'Inter',sans-serif;}
.block-container{max-width:1040px;padding-top:0 !important;padding-bottom:3rem;}
.stApp [data-testid="stMarkdownContainer"]{color:var(--text);font-family:'Inter',sans-serif;}
[data-testid="stHeading"], [data-testid="stHeading"] *{color:var(--text) !important;font-family:'Inter',sans-serif !important;font-weight:700;}
[data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] *{color:#334155 !important;font-weight:600;font-size:14px;}
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] *{color:var(--muted) !important;}
hr{border-color:var(--line) !important;}

/* navbar */
.nav{display:flex;align-items:center;margin:0 -2rem 30px;padding:16px 2rem;background:#fff;border-bottom:1px solid var(--line);}
.logo{width:36px;height:36px;border-radius:10px;background:var(--blue);display:flex;align-items:center;justify-content:center;
  font-size:18px;margin-right:12px;}
.brand{font-weight:800;font-size:19px;color:var(--text);}
.brand span{color:var(--blue);}
.nav-r{margin-left:auto;display:flex;gap:10px;align-items:center;}
.tag{padding:7px 14px;border:1px solid var(--line);border-radius:30px;background:#fff;color:#475569;font-size:13px;font-weight:600;}
.tag.ok{color:var(--green);border-color:#bbf7d0;background:#f0fdf4;}
.tag.ok i{display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--green);margin-right:7px;}

/* hero */
.hero{display:flex;align-items:center;justify-content:space-between;gap:40px;padding:52px 56px;border-radius:24px;
  background:linear-gradient(135deg,#ffffff 0%,#eef4ff 100%);border:1px solid var(--line);
  box-shadow:0 10px 30px rgba(15,23,42,.05);}
.eyebrow{display:inline-block;padding:6px 14px;border-radius:30px;background:var(--blue-l);color:var(--blue);
  font-size:12px;font-weight:700;letter-spacing:.6px;margin-bottom:20px;}
.h{font-weight:800;font-size:clamp(32px,4.6vw,52px);line-height:1.1;letter-spacing:-1.5px;color:var(--text);margin-bottom:18px;}
.h b{color:var(--blue);}
.txt{max-width:520px;color:var(--muted);font-size:16px;line-height:1.7;margin-bottom:28px;}
.stats{display:flex;gap:40px;}
.stats b{display:block;font-size:26px;font-weight:800;color:var(--text);}
.stats span{color:var(--muted);font-size:13px;}

/* hero preview card */
.preview{flex-shrink:0;width:290px;padding:22px;border-radius:18px;background:#fff;border:1px solid var(--line);
  box-shadow:0 18px 40px rgba(37,99,235,.14);}
.pv-top{display:flex;justify-content:space-between;font-size:12px;font-weight:700;color:var(--muted);letter-spacing:.8px;margin-bottom:14px;}
.pv-score{font-size:52px;font-weight:800;color:var(--green);line-height:1;}
.pv-score small{font-size:16px;color:var(--muted);font-weight:600;}
.pv-bar{height:8px;border-radius:8px;background:#e8edf5;margin:14px 0 18px;overflow:hidden;}
.pv-bar i{display:block;height:100%;width:86%;background:linear-gradient(90deg,#22c55e,#16a34a);border-radius:8px;}
.pv-row{display:flex;justify-content:space-between;font-size:13px;padding:8px 0;border-top:1px solid var(--line);color:#334155;}
.pv-row em{font-style:normal;font-weight:700;color:var(--green);}

/* feature cards */
.features{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin:22px 0 30px;}
.fcard{padding:24px;border-radius:18px;background:#fff;border:1px solid var(--line);box-shadow:0 4px 14px rgba(15,23,42,.04);}
.ficon{width:46px;height:46px;border-radius:12px;background:var(--blue-l);display:flex;align-items:center;
  justify-content:center;font-size:21px;margin-bottom:16px;}
.fcard b{display:block;font-size:16px;margin-bottom:8px;color:var(--text);}
.fcard span{display:block;color:var(--muted);font-size:14px;line-height:1.6;}

/* tabs */
div[data-baseweb="tab-list"]{gap:4px;padding:5px;background:#e9eef6;border-radius:14px;border:0;}
button[data-baseweb="tab"]{flex:1;height:44px;border-radius:10px;background:transparent;color:#475569;}
button[data-baseweb="tab"] p{color:inherit !important;font-weight:600;font-family:'Inter',sans-serif !important;}
button[data-baseweb="tab"]:hover{color:var(--text);}
button[data-baseweb="tab"][aria-selected="true"]{background:#fff;color:var(--blue);box-shadow:0 2px 8px rgba(15,23,42,.10);}
div[data-baseweb="tab-highlight"],div[data-baseweb="tab-border"]{display:none !important;}
div[data-baseweb="tab-panel"]{margin-top:16px;padding:28px !important;border-radius:18px;background:#fff;
  border:1px solid var(--line);box-shadow:0 4px 14px rgba(15,23,42,.04);}

/* inputs */
.stTextInput div[data-baseweb="input"],.stTextArea div[data-baseweb="textarea"]{
  background:#fff !important;border:1px solid #cbd5e1 !important;border-radius:10px !important;}
.stTextInput div[data-baseweb="input"]:focus-within,.stTextArea div[data-baseweb="textarea"]:focus-within{
  border-color:var(--blue) !important;box-shadow:0 0 0 3px rgba(37,99,235,.15);}
.stTextInput input,.stTextArea textarea{background:transparent !important;color:var(--text) !important;
  -webkit-text-fill-color:var(--text) !important;border:0 !important;font-family:'Inter',sans-serif !important;}
.stTextInput input::placeholder,.stTextArea textarea::placeholder{color:#94a3b8 !important;-webkit-text-fill-color:#94a3b8 !important;}

/* button */
.stButton > button{height:48px;border:0;border-radius:10px;background:var(--blue);color:#fff;font-weight:700;
  box-shadow:0 4px 12px rgba(37,99,235,.28);transition:background .15s;}
.stButton > button p{color:#fff !important;font-weight:700;font-family:'Inter',sans-serif !important;}
.stButton > button:hover{background:var(--blue-d);border:0;color:#fff;}
.stButton > button:focus:not(:active){border:0;color:#fff;}

/* results */
.result{margin-top:18px;padding:22px 24px;border-radius:14px;border:1px solid;border-left-width:6px;}
.result .label{font-size:11px;letter-spacing:1.5px;font-weight:700;color:var(--muted);}
.score{font-size:50px;font-weight:800;line-height:1.1;}
.verdict{font-size:22px;font-weight:800;margin:2px 0 4px;}
.safe{background:#f0fdf4;border-color:#86efac;border-left-color:var(--green);}
.safe .verdict,.safe .score{color:var(--green);}
.suspicious{background:#fffbeb;border-color:#fcd34d;border-left-color:var(--amber);}
.suspicious .verdict,.suspicious .score{color:var(--amber);}
.dangerous{background:#fef2f2;border-color:#fca5a5;border-left-color:var(--red);}
.dangerous .verdict,.dangerous .score{color:var(--red);}
.rtitle{color:#475569;font-size:15px;}
.signal{background:#f8fafc;border:1px solid var(--line);border-left:4px solid var(--blue);
  padding:11px 15px;margin:8px 0;border-radius:10px;font-size:14px;color:#1e293b;}

@media(max-width:850px){
  .hero{flex-direction:column;align-items:flex-start;padding:30px 24px;}
  .preview{width:100%;}
  .features{grid-template-columns:1fr;}
  .nav-r .tag:not(.ok){display:none;}
}
</style>
""", unsafe_allow_html=True)


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
            <div class="rtitle">{html.escape(title)}</div>
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

st.markdown("""
<div class="nav">
<div class="logo">🛡️</div>
<div class="brand">Cyber<span>Shield</span></div>
<div class="nav-r"><div class="tag">Rule-Based Engine</div><div class="tag ok"><i></i>System Online</div></div>
</div>
<div class="hero">
<div>
<div class="eyebrow">CYBERSECURITY ANALYZER</div>
<div class="h">Check your security <b>before</b> attackers do.</div>
<div class="txt">Analyze passwords, suspicious messages and URLs with rule-based detection. Get a clear 0-100 risk score, the warning signs found and practical recommendations.</div>
<div class="stats">
<div><b>3</b><span>Analyzers</span></div>
<div><b>0-100</b><span>Risk score</span></div>
<div><b>Instant</b><span>Results</span></div>
</div>
</div>
<div class="preview">
<div class="pv-top"><span>SAMPLE RESULT</span><span>PASSWORD</span></div>
<div class="pv-score">86<small> /100</small></div>
<div class="pv-bar"><i></i></div>
<div class="pv-row"><span>Length</span><em>Good</em></div>
<div class="pv-row"><span>Character variety</span><em>Strong</em></div>
<div class="pv-row"><span>Common password</span><em>Not found</em></div>
</div>
</div>
<div class="features">
<div class="fcard"><div class="ficon">🔐</div><b>Password Strength</b><span>Checks length, character variety, common passwords and predictable patterns.</span></div>
<div class="fcard"><div class="ficon">💬</div><b>Phishing Detection</b><span>Flags urgency, credential requests, financial lures and threatening language.</span></div>
<div class="fcard"><div class="ficon">🔗</div><b>URL Inspection</b><span>Looks at HTTPS, raw IPs, shorteners, punycode, risky endings and keywords.</span></div>
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