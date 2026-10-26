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
#MainMenu, footer, [data-testid="stToolbar"]{display:none !important;}
header[data-testid="stHeader"]{background:transparent;}
.stApp{
    background:radial-gradient(circle at 50% -20%,rgba(34,211,238,.10),transparent 40%),#080a0d;
    color:#f1f5f9;
}
.block-container{max-width:900px;padding-top:2rem;padding-bottom:3rem;}

.main-title{
    font-size:46px;font-weight:800;letter-spacing:-1.5px;margin-bottom:4px;
    background:linear-gradient(90deg,#22d3ee,#00e5a0);
    -webkit-background-clip:text;background-clip:text;color:transparent;
}
.subtitle{color:#8b949e;font-size:15px;margin-bottom:28px;}

/* tabs */
div[data-baseweb="tab-list"]{
    gap:5px;padding:5px;border:1px solid #20262d;border-radius:14px;
    background:rgba(255,255,255,.025);
}
button[data-baseweb="tab"]{flex:1;height:46px;border-radius:9px;color:#8b949e;}
button[data-baseweb="tab"]:hover{color:#fff;background:rgba(255,255,255,.04);}
button[data-baseweb="tab"][aria-selected="true"]{
    color:#22d3ee;background:rgba(34,211,238,.10);
    box-shadow:inset 0 0 0 1px rgba(34,211,238,.28);
}
div[data-baseweb="tab-highlight"],div[data-baseweb="tab-border"]{display:none !important;}

/* tab content acts as the card */
div[data-baseweb="tab-panel"]{
    margin-top:14px;padding:24px !important;border:1px solid #20262d;border-radius:18px;
    background:linear-gradient(180deg,#11151a,#0e1115);
}

/* inputs */
.stTextInput label,.stTextArea label{color:#aeb7c2 !important;font-size:13px !important;}
.stTextInput div[data-baseweb="input"],.stTextArea div[data-baseweb="textarea"]{
    background:#090b0e !important;border:1px solid #252b33 !important;border-radius:11px !important;
}
.stTextInput div[data-baseweb="input"]:focus-within,
.stTextArea div[data-baseweb="textarea"]:focus-within{
    border-color:#22d3ee !important;box-shadow:0 0 0 3px rgba(34,211,238,.08);
}
.stTextInput input,.stTextArea textarea{
    background:transparent !important;color:#fff !important;border:0 !important;
}

/* button */
.stButton > button{
    height:48px;border:0;border-radius:11px;font-weight:700;color:#031012;
    background:linear-gradient(90deg,#25cbe5,#00e4a0);
}
.stButton > button:hover,
.stButton > button:focus:not(:active){color:#031012;border:0;filter:brightness(1.08);}

/* results */
.result{margin-top:16px;padding:20px;border-radius:14px;border:1px solid;}
.result .label{font-size:11px;letter-spacing:1.5px;color:#8b949e;}
.score{font-size:46px;font-weight:800;line-height:1.1;}
.result h2{margin:2px 0 4px;padding:0;}
.safe{background:rgba(0,229,160,.07);border-color:rgba(0,229,160,.4);}
.safe h2,.safe .score{color:#00e5a0;}
.suspicious{background:rgba(255,176,32,.07);border-color:rgba(255,176,32,.4);}
.suspicious h2,.suspicious .score{color:#ffb020;}
.dangerous{background:rgba(255,77,109,.07);border-color:rgba(255,77,109,.4);}
.dangerous h2,.dangerous .score{color:#ff4d6d;}
.signal{
    background:#0e1115;border:1px solid #1d232a;border-left:4px solid #ffb020;
    padding:11px 14px;margin:8px 0;border-radius:9px;font-size:13px;color:#c8d0d8;
}
h1,h2,h3,h4{color:#f1f5f9 !important;}
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
            <h2>{html.escape(verdict)}</h2>
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

st.markdown('<div class="main-title">🛡️ CyberShield</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="subtitle">AI-Inspired Cybersecurity Risk Analyzer • Rule-Based Security Engine</div>',
    unsafe_allow_html=True,
)

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