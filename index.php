<?php
$allowedThemes = ["cyber", "purple", "light"];

if (isset($_GET["theme"]) && in_array($_GET["theme"], $allowedThemes, true)) {
    $theme = $_GET["theme"];
    setcookie("cs_theme", $theme, time() + 60 * 60 * 24 * 365, "/");
} elseif (isset($_COOKIE["cs_theme"]) && in_array($_COOKIE["cs_theme"], $allowedThemes, true)) {
    $theme = $_COOKIE["cs_theme"];
} else {
    $theme = "cyber";
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>CyberShield — Security Analyzer</title>

    <link rel="stylesheet" href="style.php?theme=<?= htmlspecialchars($theme) ?>">
</head>

<body>

<div class="wrap">

    <header>

        <div class="logo">🛡️</div>

        <div class="brand">
            <b>CyberShield</b>
            <small>Security Analyzer</small>
        </div>

        <div class="header-right">

            <div class="themes" aria-label="Choose theme">
                <?php foreach ($allowedThemes as $t): ?>
                    <a
                        href="?theme=<?= $t ?>"
                        class="theme-dot <?= $t ?> <?= $t === $theme ? 'active' : '' ?>"
                        title="<?= ucfirst($t) ?> theme"
                        aria-label="<?= ucfirst($t) ?> theme">
                    </a>
                <?php endforeach; ?>
            </div>

            <div class="status">
                <span></span>
                System Online
            </div>

        </div>

    </header>


    <main>

        <h1>
            Stay Safe.
            <em>Detect Threats</em>
        </h1>

        <p class="lead">
            Analyze passwords, suspicious messages and URLs
            using rule-based cybersecurity detection.
        </p>


        <!-- TABS -->
        <div class="tabs">
            <button type="button" class="tab active" data-type="password">🔐 Password</button>
            <button type="button" class="tab" data-type="message">💬 Message</button>
            <button type="button" class="tab" data-type="url">🔗 URL</button>
        </div>


        <!-- PASSWORD PANEL -->
        <section id="passwordPanel" class="panel active">
            <div class="card">

                <label for="password">Password</label>

                <div class="password-box">
                    <input
                        id="password"
                        type="password"
                        placeholder="Enter password"
                        autocomplete="new-password">

                    <button type="button" id="showPassword">👁</button>
                </div>

                <div class="requirements">
                    <span id="length">✕ 12+ characters</span>
                    <span id="upper">✕ Uppercase</span>
                    <span id="lower">✕ Lowercase</span>
                    <span id="number">✕ Number</span>
                    <span id="special">✕ Special character</span>
                </div>

                <button type="button" id="passwordButton" class="analyze">
                    🔍 Analyze Password
                </button>

                <div class="privacy-note">
                    🔒 Password analysis is performed locally
                    through the PHP security engine.
                    The password is not stored.
                </div>

            </div>
        </section>


        <!-- MESSAGE PANEL -->
        <section id="messagePanel" class="panel">
            <div class="card">

                <label for="message">Message / Email / SMS</label>

                <textarea
                    id="message"
                    maxlength="5000"
                    placeholder="Paste a suspicious message, email or SMS here..."></textarea>

                <div class="counter">
                    <span id="count">0</span> / 5000
                </div>

                <button type="button" id="messageButton" class="analyze">
                    🔍 Analyze Message
                </button>

                <div class="privacy-note">
                    🛡️ Checks phishing, urgency,
                    credential, financial and suspicious-link indicators.
                </div>

            </div>
        </section>


        <!-- URL PANEL -->
        <section id="urlPanel" class="panel">
            <div class="card">

                <label for="url">Website URL</label>

                <input
                    id="url"
                    type="text"
                    placeholder="https://example.com"
                    autocomplete="off">

                <button type="button" id="urlButton" class="analyze">
                    🔍 Scan URL
                </button>

                <div class="privacy-note">
                    🔗 Checks HTTPS, IP addresses,
                    URL shorteners, punycode, suspicious
                    patterns and domain structure.
                </div>

            </div>
        </section>


        <!-- RESULT -->
        <div id="result"></div>

    </main>


    <footer>
        CyberShield · B.Sc IT Cyber Security Project
    </footer>

</div>

<script src="script.js"></script>

</body>
</html>