import streamlit as st
import re
from urllib.parse import urlparse

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CyberShield AI Security Analyzer",
    page_icon="🛡️",
    layout="wide"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>
    .stApp {
        background: #0B0B0C;
        color: #F3F3F4;
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .subtitle {
        color: #8E8E93;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .card {
        background: #121214;
        border: 1px solid #1C1C1E;
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 20px;
    }

    .safe {
        background: #12351F;
        border: 1px solid #27AE60;
        padding: 18px;
        border-radius: 12px;
    }

    .suspicious {
        background: #3A2D0B;
        border: 1px solid #F2C94C;
        padding: 18px;
        border-radius: 12px;
    }

    .dangerous {
        background: #3A1111;
        border: 1px solid #EB5757;
        padding: 18px;
        border-radius: 12px;
    }

    .score {
        font-size: 46px;
        font-weight: 800;
    }

    .signal {
        background: #18181B;
        border-left: 4px solid #FF5436;
        padding: 12px;
        margin: 8px 0;
        border-radius: 6px;
    }

    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }

    h1, h2, h3 {
        color: #F3F3F4 !important;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# PASSWORD ANALYZER
# ============================================================

def analyze_password(password):

    score = 0
    signals = []
    recommendations = []

    length = len(password)

    # Length
    if length >= 16:
        score += 30
        signals.append("Excellent password length.")
    elif length >= 12:
        score += 24
        signals.append("Good password length.")
    elif length >= 8:
        score += 15
        signals.append("Password length is acceptable.")
    else:
        signals.append("Password is too short.")

    # Character types
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

    # Repeated characters
    if re.search(r"(.)\1\1", password):
        score -= 15
        signals.append("Repeated characters detected.")

    # Sequential patterns
    sequences = [
        "123456",
        "234567",
        "345678",
        "abcdef",
        "qwerty",
        "asdfgh",
        "password"
    ]

    lower = password.lower()

    for seq in sequences:
        if seq in lower:
            score -= 25
            signals.append("Common sequence detected.")
            break

    # Common passwords
    common = {
        "password",
        "123456",
        "12345678",
        "qwerty",
        "admin",
        "letmein",
        "welcome",
        "iloveyou",
        "password123",
        "admin123"
    }

    if lower in common:
        score = 5
        signals.append("This is a commonly used password.")
        recommendations.append("Use a completely unique password.")

    # Year/date pattern
    if re.search(r"(19|20)\d{2}", password):
        score -= 5
        signals.append("A year-like pattern was detected.")

    score = max(0, min(100, score))

    if score >= 75:
        verdict = "SAFE"
        title = "Strong Password"
        css = "safe"
    elif score >= 45:
        verdict = "SUSPICIOUS"
        title = "Moderate Password"
        css = "suspicious"
    else:
        verdict = "DANGEROUS"
        title = "Weak Password"
        css = "dangerous"

    if not recommendations:
        recommendations.append("Keep this password unique and never reuse it.")

    return score, verdict, title, signals, recommendations, css


# ============================================================
# MESSAGE ANALYZER
# ============================================================

def analyze_message(message):

    text = message.lower()

    score = 0
    signals = []
    recommendations = []

    phishing_words = [
        "verify your account",
        "verify account",
        "click here",
        "confirm your account",
        "account suspended",
        "account blocked",
        "login immediately",
        "security alert",
        "unusual activity"
    ]

    urgency_words = [
        "urgent",
        "immediately",
        "now",
        "act now",
        "within 24 hours",
        "limited time",
        "final warning"
    ]

    credential_words = [
        "password",
        "otp",
        "one time password",
        "verification code",
        "login",
        "username",
        "pin"
    ]

    financial_words = [
        "bank",
        "credit card",
        "debit card",
        "payment",
        "refund",
        "money",
        "upi",
        "transaction",
        "wallet"
    ]

    threat_words = [
        "suspended",
        "blocked",
        "legal action",
        "police",
        "penalty",
        "fine"
    ]

    # Phishing
    found = [x for x in phishing_words if x in text]

    if found:
        score += 25
        signals.append("Phishing-style language detected.")

    # Urgency
    found = [x for x in urgency_words if x in text]

    if found:
        score += 15
        signals.append("Urgency or pressure detected.")

    # Credentials
    found = [x for x in credential_words if x in text]

    if found:
        score += 20
        signals.append("Message requests or mentions sensitive credentials.")

    # Financial
    found = [x for x in financial_words if x in text]

    if found:
        score += 15
        signals.append("Financial/payment-related language detected.")

    # Threats
    found = [x for x in threat_words if x in text]

    if found:
        score += 15
        signals.append("Threatening or account-lock language detected.")

    # URLs
    urls = re.findall(r"https?://[^\s]+|www\.[^\s]+", text)

    if urls:
        score += 15
        signals.append("URL/link detected in the message.")

    # Combination bonus
    if (
        ("password" in text or "otp" in text)
        and ("click" in text or "link" in text)
    ):
        score += 15
        signals.append("Credential request combined with a link.")

    score = max(0, min(100, score))

    if score >= 60:
        verdict = "DANGEROUS"
        title = "Likely Phishing / Scam"
        css = "dangerous"
    elif score >= 30:
        verdict = "SUSPICIOUS"
        title = "Suspicious Message"
        css = "suspicious"
    else:
        verdict = "SAFE"
        title = "No Major Red Flags"
        css = "safe"

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

    if not original:
        return 0, "DANGEROUS", "Invalid URL", ["No URL provided."], [], "dangerous"

    if not re.match(r"^https?://", original, re.I):
        url_to_parse = "http://" + original
    else:
        url_to_parse = original

    try:
        parsed = urlparse(url_to_parse)
        host = parsed.hostname or ""
        path = parsed.path.lower()
    except Exception:
        return 80, "DANGEROUS", "Invalid URL", ["URL could not be parsed."], [], "dangerous"

    full_lower = original.lower()

    # HTTPS
    if original.lower().startswith("https://"):
        signals.append("HTTPS is enabled.")
    else:
        score += 20
        signals.append("HTTPS is not used.")

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

    # Shorteners
    shorteners = [
        "bit.ly",
        "tinyurl.com",
        "t.co",
        "goo.gl",
        "is.gd",
        "ow.ly",
        "buff.ly"
    ]

    if any(x in host for x in shorteners):
        score += 20
        signals.append("URL shortener detected.")

    # Suspicious TLD
    suspicious_tlds = [
        ".tk",
        ".ml",
        ".ga",
        ".cf",
        ".gq",
        ".click",
        ".top",
        ".xyz"
    ]

    if any(host.endswith(tld) for tld in suspicious_tlds):
        score += 15
        signals.append("Higher-risk/suspicious TLD detected.")

    # Too many subdomains
    if host.count(".") >= 4:
        score += 15
        signals.append("Unusually high number of subdomains.")

    # Long URL
    if len(original) > 120:
        score += 10
        signals.append("Unusually long URL.")

    # Suspicious words
    suspicious_words = [
        "login",
        "verify",
        "verification",
        "secure",
        "account",
        "update",
        "password",
        "wallet",
        "payment",
        "free",
        "claim",
        "bonus",
        "gift",
        "confirm"
    ]

    matches = [word for word in suspicious_words if word in full_lower]

    if len(matches) >= 2:
        score += 15
        signals.append("Multiple suspicious URL keywords detected.")

    # Encoded characters
    if "%" in original:
        score += 5
        signals.append("Encoded URL characters detected.")

    # Multiple hyphens
    if host.count("-") >= 3:
        score += 10
        signals.append("Domain contains many hyphens.")

    score = max(0, min(100, score))

    if score >= 55:
        verdict = "DANGEROUS"
        title = "High-Risk URL"
        css = "dangerous"
    elif score >= 25:
        verdict = "SUSPICIOUS"
        title = "Suspicious URL"
        css = "suspicious"
    else:
        verdict = "SAFE"
        title = "No Major URL Red Flags"
        css = "safe"

    recommendations.append("Check the domain name carefully before entering credentials.")

    if not original.lower().startswith("https://"):
        recommendations.append("Prefer HTTPS websites.")

    recommendations.append(
        "Static URL analysis cannot guarantee that a website is legitimate."
    )

    return score, verdict, title, signals, recommendations, css


# ============================================================
# RESULT DISPLAY
# ============================================================

def show_result(result):

    score, verdict, title, signals, recommendations, css = result

    st.markdown(
        f"""
        <div class="{css}">
            <div style="font-size:14px;color:#B8B8BC;">SECURITY VERDICT</div>
            <div class="score">{score}/100</div>
            <h2>{verdict}</h2>
            <p style="font-size:18px;">{title}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🔎 Security Signals")

    if signals:
        for signal in signals:
            st.markdown(
                f'<div class="signal">⚠️ {signal}</div>',
                unsafe_allow_html=True
            )
    else:
        st.success("No major suspicious indicators were detected.")

    st.markdown("### 🛡️ Recommendations")

    for recommendation in recommendations:
        st.markdown(f"- {recommendation}")


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🛡️ CyberShield</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-Inspired Cybersecurity Risk Analyzer • Rule-Based Security Engine</div>',
    unsafe_allow_html=True
)

# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3 = st.tabs([
    "🔐 Password Analyzer",
    "💬 Message Analyzer",
    "🔗 URL Analyzer"
])


# ============================================================
# PASSWORD TAB
# ============================================================

with tab1:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Password Security Analysis")

    password = st.text_input(
        "Enter a password to analyze",
        type="password",
        placeholder="Enter password..."
    )

    if st.button("🔍 Analyze Password", key="password_btn", use_container_width=True):

        if not password:
            st.warning("Please enter a password.")
        else:
            result = analyze_password(password)
            show_result(result)

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# MESSAGE TAB
# ============================================================

with tab2:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Phishing & Scam Message Analysis")

    message = st.text_area(
        "Paste the message here",
        height=220,
        placeholder="Example: Your account has been suspended. Click here to verify..."
    )

    st.caption(f"Characters: {len(message)}")

    if st.button("🔍 Analyze Message", key="message_btn", use_container_width=True):

        if not message.strip():
            st.warning("Please enter a message.")
        else:
            result = analyze_message(message)
            show_result(result)

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# URL TAB
# ============================================================

with tab3:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Website / URL Security Analysis")

    url = st.text_input(
        "Enter a URL",
        placeholder="https://example.com"
    )

    if st.button("🔍 Analyze URL", key="url_btn", use_container_width=True):

        if not url.strip():
            st.warning("Please enter a URL.")
        else:
            result = analyze_url(url)
            show_result(result)

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "CyberShield uses rule-based static analysis. "
    "Results are indicators, not a 100% guarantee of safety."
)