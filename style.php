<?php
header("Content-Type: text/css; charset=UTF-8");

$themes = [
    "cyber" => [
        "bg" => "#080a0d", "panel" => "#101318",
        "card1" => "#11151a", "card2" => "#0e1115",
        "border" => "#20262d", "input_bg" => "#090b0e", "input_border" => "#252b33",
        "text" => "#f1f5f9", "muted" => "#8b949e", "label" => "#aeb7c2",
        "subtle" => "#6f7882", "signal_name" => "#c8d0d8", "body_text" => "#9ca7b2",
        "cyan" => "#22d3ee", "green" => "#00e5a0",
        "yellow" => "#ffb020", "red" => "#ff4d6d",
        "cyan_rgb" => "34,211,238", "green_rgb" => "0,229,160",
        "overlay_rgb" => "255,255,255", "btn_text" => "#031012",
    ],
    "purple" => [
        "bg" => "#0b0814", "panel" => "#150f24",
        "card1" => "#1a1330", "card2" => "#130e24",
        "border" => "#2b2145", "input_bg" => "#0e0a1b", "input_border" => "#33285a",
        "text" => "#f5f3ff", "muted" => "#9d94c0", "label" => "#b9b0dc",
        "subtle" => "#8077a6", "signal_name" => "#d6d0f0", "body_text" => "#b0a8d4",
        "cyan" => "#a78bfa", "green" => "#f472b6",
        "yellow" => "#fbbf24", "red" => "#fb7185",
        "cyan_rgb" => "167,139,250", "green_rgb" => "244,114,182",
        "overlay_rgb" => "255,255,255", "btn_text" => "#1a0b2e",
    ],
    "light" => [
        "bg" => "#f4f6f9", "panel" => "#ffffff",
        "card1" => "#ffffff", "card2" => "#f9fafc",
        "border" => "#dde3ea", "input_bg" => "#ffffff", "input_border" => "#c9d2dc",
        "text" => "#0f172a", "muted" => "#5b6675", "label" => "#334155",
        "subtle" => "#64748b", "signal_name" => "#1e293b", "body_text" => "#475569",
        "cyan" => "#0284c7", "green" => "#059669",
        "yellow" => "#d97706", "red" => "#dc2626",
        "cyan_rgb" => "2,132,199", "green_rgb" => "5,150,105",
        "overlay_rgb" => "0,0,0", "btn_text" => "#ffffff",
    ],
];

$name = $_GET["theme"] ?? "cyber";
$t = $themes[$name] ?? $themes["cyber"];
?>
:root {
    --bg: <?= $t["bg"] ?>;
    --panel: <?= $t["panel"] ?>;
    --card1: <?= $t["card1"] ?>;
    --card2: <?= $t["card2"] ?>;
    --border: <?= $t["border"] ?>;
    --input-bg: <?= $t["input_bg"] ?>;
    --input-border: <?= $t["input_border"] ?>;
    --text: <?= $t["text"] ?>;
    --muted: <?= $t["muted"] ?>;
    --label: <?= $t["label"] ?>;
    --subtle: <?= $t["subtle"] ?>;
    --signal-name: <?= $t["signal_name"] ?>;
    --body-text: <?= $t["body_text"] ?>;
    --cyan: <?= $t["cyan"] ?>;
    --green: <?= $t["green"] ?>;
    --yellow: <?= $t["yellow"] ?>;
    --red: <?= $t["red"] ?>;
    --cyan-rgb: <?= $t["cyan_rgb"] ?>;
    --green-rgb: <?= $t["green_rgb"] ?>;
    --overlay-rgb: <?= $t["overlay_rgb"] ?>;
    --btn-text: <?= $t["btn_text"] ?>;
}

* { box-sizing: border-box; }

body {
    margin: 0;
    min-height: 100vh;
    background:
        radial-gradient(circle at 50% -20%, rgba(var(--cyan-rgb), .12), transparent 40%),
        var(--bg);
    color: var(--text);
    font-family: Arial, Helvetica, sans-serif;
}

.wrap {
    width: min(900px, calc(100% - 36px));
    margin: auto;
    padding: 30px 0 50px;
}

header {
    display: flex;
    align-items: center;
    margin-bottom: 60px;
}

.logo {
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 13px;
    background: linear-gradient(135deg, var(--cyan), var(--green));
    margin-right: 12px;
}

.brand b { display: block; font-size: 20px; }
.brand small { color: var(--muted); font-size: 12px; }

.header-right {
    margin-left: auto;
    display: flex;
    align-items: center;
    gap: 10px;
}

.themes {
    display: flex;
    gap: 6px;
    padding: 4px;
    border: 1px solid var(--border);
    border-radius: 30px;
    background: rgba(var(--overlay-rgb), .03);
}

.theme-dot {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    border: 2px solid transparent;
    display: block;
    transition: transform .15s;
}
.theme-dot:hover { transform: scale(1.15); }
.theme-dot.active { border-color: var(--text); }
.theme-dot.cyber  { background: linear-gradient(135deg, #22d3ee, #00e5a0); }
.theme-dot.purple { background: linear-gradient(135deg, #a78bfa, #f472b6); }
.theme-dot.light  { background: linear-gradient(135deg, #f4f6f9, #0284c7); }

.status {
    padding: 8px 14px;
    border: 1px solid rgba(var(--green-rgb), .35);
    border-radius: 30px;
    color: var(--green);
    font-size: 12px;
}

.status span {
    display: inline-block;
    width: 7px;
    height: 7px;
    margin-right: 7px;
    border-radius: 50%;
    background: var(--green);
}

h1 {
    margin: 0;
    font-size: clamp(38px, 6vw, 58px);
    letter-spacing: -2px;
}

h1 em {
    font-style: normal;
    background: linear-gradient(90deg, var(--cyan), var(--green));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.lead {
    color: var(--muted);
    line-height: 1.6;
    margin: 18px 0 32px;
}

.tabs {
    display: flex;
    gap: 5px;
    padding: 5px;
    margin-bottom: 14px;
    border: 1px solid var(--border);
    border-radius: 14px;
    background: rgba(var(--overlay-rgb), .025);
}

.tab {
    flex: 1;
    height: 46px;
    border: 0;
    border-radius: 9px;
    background: transparent;
    color: var(--muted);
    cursor: pointer;
    font-size: 14px;
}

.tab:hover {
    color: var(--text);
    background: rgba(var(--overlay-rgb), .05);
}

.tab.active {
    color: var(--cyan);
    background: rgba(var(--cyan-rgb), .1);
    box-shadow: inset 0 0 0 1px rgba(var(--cyan-rgb), .28);
}

.panel { display: none; }
.panel.active { display: block; }

.card {
    padding: 24px;
    border: 1px solid var(--border);
    border-radius: 18px;
    background: linear-gradient(180deg, var(--card1), var(--card2));
}

label {
    display: block;
    margin-bottom: 9px;
    color: var(--label);
    font-size: 13px;
}

input,
textarea {
    width: 100%;
    border: 1px solid var(--input-border);
    border-radius: 11px;
    outline: none;
    background: var(--input-bg);
    color: var(--text);
    font-family: inherit;
    font-size: 15px;
}

input { height: 48px; padding: 0 14px; }
textarea { min-height: 180px; padding: 14px; resize: vertical; }

input:focus,
textarea:focus {
    border-color: var(--cyan);
    box-shadow: 0 0 0 3px rgba(var(--cyan-rgb), .12);
}

.password-box { position: relative; }
.password-box input { padding-right: 50px; }

.password-box button {
    position: absolute;
    top: 50%;
    right: 8px;
    transform: translateY(-50%);
    border: 0;
    background: transparent;
    color: var(--muted);
    cursor: pointer;
}

.requirements {
    display: flex;
    flex-wrap: wrap;
    gap: 7px;
    margin-top: 12px;
}

.requirements span {
    padding: 6px 10px;
    border: 1px solid var(--input-border);
    border-radius: 50px;
    color: var(--subtle);
    font-size: 11px;
}

.requirements span.good {
    color: var(--green);
    border-color: rgba(var(--green-rgb), .3);
    background: rgba(var(--green-rgb), .06);
}

.analyze {
    width: 100%;
    height: 48px;
    margin-top: 17px;
    border: 0;
    border-radius: 11px;
    background: linear-gradient(90deg, var(--cyan), var(--green));
    color: var(--btn-text);
    font-weight: bold;
    cursor: pointer;
}

.analyze:hover { filter: brightness(1.08); }
.analyze:disabled { opacity: .6; cursor: wait; }

.privacy-note {
    margin-top: 13px;
    color: var(--subtle);
    font-size: 11px;
    line-height: 1.5;
}

.counter {
    margin-top: 6px;
    text-align: right;
    color: var(--subtle);
    font-size: 11px;
}

#result { margin-top: 16px; }

.result-card {
    padding: 23px;
    border: 1px solid var(--border);
    border-radius: 18px;
    background: var(--panel);
}

.result-top {
    display: flex;
    align-items: center;
    gap: 18px;
}

.score-box {
    width: 90px;
    height: 90px;
    flex-shrink: 0;
    display: flex;
    align-items: baseline;
    justify-content: center;
    border: 5px solid var(--cyan);
    border-radius: 50%;
}

.score-box strong { margin-top: 28px; font-size: 25px; }
.score-box span { color: var(--muted); font-size: 11px; }
.score-box.safe { border-color: var(--green); }
.score-box.suspicious { border-color: var(--yellow); }
.score-box.dangerous { border-color: var(--red); }

.result-label {
    color: var(--muted);
    font-size: 10px;
    letter-spacing: 1.5px;
}

.result-heading h2 { margin: 5px 0; }
.result-heading h2.safe { color: var(--green); }
.result-heading h2.suspicious { color: var(--yellow); }
.result-heading h2.dangerous { color: var(--red); }

.result-heading p {
    margin: 0;
    color: var(--muted);
    font-size: 12px;
}

.analysis-box {
    margin-top: 22px;
    padding: 15px;
    border-left: 3px solid var(--cyan);
    background: rgba(var(--cyan-rgb), .05);
}

.analysis-title { font-weight: bold; margin-bottom: 7px; }

.analysis-box p {
    margin: 0;
    color: var(--body-text);
    line-height: 1.6;
    font-size: 13px;
}

.section-title {
    margin: 22px 0 9px;
    color: var(--subtle);
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 1.4px;
}

.signal {
    display: flex;
    align-items: center;
    gap: 10px;
    min-height: 42px;
    margin-bottom: 6px;
    padding: 8px 11px;
    border: 1px solid var(--border);
    border-radius: 9px;
    font-size: 12px;
}

.signal-icon { width: 20px; font-weight: bold; }
.signal.good .signal-icon { color: var(--green); }
.signal.warning .signal-icon { color: var(--yellow); }
.signal.bad .signal-icon { color: var(--red); }

.signal-name { color: var(--signal-name); }

.signal-detail {
    margin-left: auto;
    color: var(--subtle);
    font-size: 11px;
}

.tips {
    color: var(--body-text);
    line-height: 1.8;
    font-size: 13px;
}

.error-card {
    display: flex;
    gap: 13px;
    border-color: rgba(255, 77, 109, .35);
}

.error-icon { font-size: 22px; }
.error-card strong { color: var(--red); }
.error-card p { color: var(--muted); font-size: 12px; }

.loading-card {
    display: flex;
    align-items: center;
    gap: 14px;
}

.loading-spinner {
    width: 25px;
    height: 25px;
    border: 3px solid var(--border);
    border-top-color: var(--cyan);
    border-radius: 50%;
    animation: spin .8s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

footer {
    margin-top: 30px;
    text-align: center;
    color: var(--subtle);
    font-size: 11px;
}

@media (max-width: 600px) {
    .wrap { width: calc(100% - 24px); }
    .status { display: none; }
    .card { padding: 17px; }
    .result-top { align-items: flex-start; }
    .score-box { width: 75px; height: 75px; }
}