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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap');

:root{
  --bg:#05060a; --line:rgba(255,255,255,.08); --text:#e6e6f0; --muted:#9a9db3;
  --cyan:#22d3ee; --violet:#8b5cf6; --pink:#f472b6; --green:#34d399; --amber:#fbbf24; --red:#fb7185;
}
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"]{display:none !important;}
header[data-testid="stHeader"]{background:transparent;}

.stApp{
  background:
    radial-gradient(900px 500px at 100% 0%, rgba(124,58,237,.20), transparent 60%),
    radial-gradient(700px 420px at 0% 10%, rgba(34,211,238,.08), transparent 60%),
    var(--bg);
  color:var(--text);
  font-family:'Inter',sans-serif;
}
.block-container{max-width:1120px;padding-top:1.2rem;padding-bottom:3rem;}
h1,h2,h3,h4,h5{font-family:'Space Grotesk',sans-serif !important;color:var(--text) !important;}

/* top nav */
.nav{display:flex;align-items:center;margin-bottom:22px;}
.nav-logo{width:34px;height:34px;border-radius:10px;display:flex;align-items:center;justify-content:center;
  background:linear-gradient(135deg,#22d3ee,#8b5cf6);margin-right:12px;font-size:17px;}
.nav-brand{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:20px;color:#fff;}
.nav-brand .c{color:var(--cyan);} .nav-brand .v{color:var(--violet);}
.nav-pills{margin-left:auto;display:flex;gap:10px;}
.pill{padding:8px 16px;border:1px solid var(--line);border-radius:30px;background:rgba(255,255,255,.03);
  color:#cfd2e6;font-size:13px;font-weight:600;}
.pill i{display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--green);margin-right:8px;}

/* hero */
.hero{
  position:relative;overflow:hidden;display:flex;align-items:center;justify-content:space-between;gap:30px;
  padding:56px 60px;border:1px solid var(--line);border-radius:30px;
  background:
    linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px) 0 0/44px 44px,
    linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px) 0 0/44px 44px,
    linear-gradient(135deg,rgba(76,45,140,.45),rgba(8,24,34,.75));
}
.badge{display:inline-block;padding:8px 16px;border:1px solid rgba(34,211,238,.35);border-radius:30px;
  background:rgba(34,211,238,.08);color:#7ee7f7;font-size:12px;font-weight:700;letter-spacing:.6px;margin-bottom:26px;}
.hero-title{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:clamp(40px,5.2vw,66px);
  line-height:1.05;letter-spacing:-2px;color:#c9c9d8;margin:0 0 22px;}
.grad{background:linear-gradient(90deg,#22d3ee,#8b5cf6,#f472b6);-webkit-background-clip:text;
  background-clip:text;color:transparent;}
.hero-text{max-width:520px;color:#a9acc2;font-size:17px;line-height:1.7;margin:0 0 30px;}
.stats{display:flex;gap:42px;}
.stats b{display:block;font-family:'Space Grotesk',sans-serif;font-size:26px;color:#fff;}
.stats span{color:var(--muted);font-size:13px;}

/* orbit graphic */
.orbit{position:relative;width:300px;height:300px;flex-shrink:0;}
.ring{position:absolute;border-radius:50%;border:1px solid rgba(34,211,238,.35);}
.r1{inset:0;} .r2{inset:52px;border-color:rgba(139,92,246,.30);}
.sphere{position:absolute;inset:108px;border-radius:50%;
  background:radial-gradient(circle at 35% 30%,#67e8f9,#8b5cf6 70%);
  box-shadow:0 0 70px rgba(99,102,241,.55);}
.tag{position:absolute;padding:7px 14px;border:1px solid var(--line);border-radius:30px;background:#0b0d14;
  color:#fff;font-size:12px;font-weight:700;white-space:nowrap;}
.tag i{display:inline-block;width:6px;height:6px;border-radius:50%;margin-right:8px;}
.t1{top:-4px;left:-8px;} .t1 i{background:var(--cyan);}
.t2{top:46%;right:-34px;} .t2 i{background:var(--violet);}
.t3{bottom:12px;left:-20px;} .t3 i{background:var(--pink);}

/* feature cards */
.features{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin:24px 0 30px;}
.fcard{padding:26px;border:1px solid var(--line);border-radius:22px;background:rgba(255,255,255,.025);}
.ficon{width:48px;height:48px;border-radius:14px;display:flex;align-items:center;justify-content:center;
  background:linear-gradient(135deg,rgba(34,211,238,.15),rgba(139,92,246,.2));border:1px solid var(--line);
  font-size:22px;margin-bottom:22px;}
.fcard h4{margin:0 0 10px;font-size:17px;}
.fcard p{margin:0;color:var(--muted);font-size:14px;line-height:1.6;}

/* tabs */
div[data-baseweb="tab-list"]{gap:6px;padding:6px;border:1px solid var(--line);border-radius:16px;background:rgba(255,255,255,.025);}
button[data-baseweb="tab"]{flex:1;height:46px;border-radius:11px;color:var(--muted);font-weight:600;}
button[data-baseweb="tab"]:hover{color:#fff;background:rgba(255,255,255,.04);}
button[data-baseweb="tab"][aria-selected="true"]{color:#fff;
  background:linear-gradient(90deg,rgba(34,211,238,.16),rgba(139,92,246,.22));
  box-shadow:inset 0 0 0 1px rgba(139,92,246,.45);}
div[data-baseweb="tab-highlight"],div[data-baseweb="tab-border"]{display:none !important;}
div[data-baseweb="tab-panel"]{margin-top:14px;padding:28px !important;border:1px solid var(--line);
  border-radius:24px;background:linear-gradient(180deg,rgba(255,255,255,.035),rgba(255,255,255,.015));}

/* inputs */
.stTextInput label,.stTextArea label{color:#b4b7cc !important;font-size:13px !important;}
.stTextInput div[data-baseweb="input"],.stTextArea div[data-baseweb="textarea"]{
  background:#07080d !important;border:1px solid rgba(255,255,255,.10) !important;border-radius:13px !important;}
.stTextInput div[data-baseweb="input"]:focus-within,.stTextArea div[data-baseweb="textarea"]:focus-within{
  border-color:var(--violet) !important;box-shadow:0 0 0 3px rgba(139,92,246,.18);}
.stTextInput input,.stTextArea textarea{background:transparent !important;color:#fff !important;border:0 !important;}

/* button */
.stButton > button{height:50px;border:0;border-radius:13px;font-weight:700;color:#fff;
  background:linear-gradient(90deg,#0ea5e9,#8b5cf6 60%,#ec4899);}
.stButton > button:hover,.stButton > button:focus:not(:active){color:#fff;border:0;filter:brightness(1.12);
  box-shadow:0 8px 30px rgba(139,92,246,.35);}

/* results */
.result{margin-top:18px;padding:22px;border-radius:18px;border:1px solid;}
.result .label{font-size:11px;letter-spacing:1.5px;color:var(--muted);}
.score{font-family:'Space Grotesk',sans-serif;font-size:50px;font-weight:700;line-height:1.1;}
.result h2{margin:2px 0 4px;padding:0;}
.safe{background:rgba(52,211,153,.07);border-color:rgba(52,211,153,.4);} .safe h2,.safe .score{color:var(--green) !important;}
.suspicious{background:rgba(251,191,36,.07);border-color:rgba(251,191,36,.4);} .suspicious h2,.suspicious .score{color:var(--amber) !important;}
.dangerous{background:rgba(251,113,133,.07);border-color:rgba(251,113,133,.4);} .dangerous h2,.dangerous .score{color:var(--red) !important;}
.signal{background:rgba(255,255,255,.03);border:1px solid var(--line);border-left:4px solid var(--violet);
  padding:12px 15px;margin:8px 0;border-radius:11px;font-size:13px;color:#d3d6e6;}

@media(max-width:900px){
  .hero{flex-direction:column;align-items:flex-start;padding:34px 26px;}
  .orbit{display:none;}
  .features{grid-template-columns:1fr;}
  .nav-pills{display:none;}
  .stats{gap:26px;}
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

st.markdown("""
<div class="nav">
<div class="nav-logo">🛡️</div>
<div class="nav-brand">Cyber <span class="c">Shield</span> <span class="v">AI</span></div>
<div class="nav-pills"><div class="pill"><i></i>Rule-Based Engine</div><div class="pill">Static Analysis</div></div>
</div>
<div class="hero">
<div>
<div class="badge">✦ CYBERSECURITY INTELLIGENCE</div>
<h1 class="hero-title">See how safe your<br>data <span class="grad">really</span><br>is.</h1>
<p class="hero-text">Analyze passwords, suspicious messages and URLs with rule-based detection, get a 0-100 risk score and clear recommendations in seconds.</p>
<div class="stats">
<div><b>3</b><span>Analyzers</span></div>
<div><b>0-100</b><span>Risk score</span></div>
<div><b>Instant</b><span>Results</span></div>
</div>
</div>
<div class="orbit">
<div class="ring r1"></div><div class="ring r2"></div><div class="sphere"></div>
<div class="tag t1"><i></i>Password</div>
<div class="tag t2"><i></i>Message</div>
<div class="tag t3"><i></i>URL</div>
</div>
</div>
<div class="features">
<div class="fcard"><div class="ficon">🔐</div><h4>Password Strength</h4><p>Checks length, character variety, common passwords and predictable patterns.</p></div>
<div class="fcard"><div class="ficon">💬</div><h4>Phishing Detection</h4><p>Flags urgency, credential requests, financial lures and threatening language.</p></div>
<div class="fcard"><div class="ficon">🔗</div><h4>URL Inspection</h4><p>Looks at HTTPS, raw IPs, shorteners, punycode, risky endings and keywords.</p></div>
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