<?php

header("Content-Type: application/json");

if ($_SERVER["REQUEST_METHOD"] !== "POST") {

    echo json_encode([
        "success" => false,
        "error" => "POST request required."
    ]);

    exit;
}


$type =
    $_POST["type"] ?? "";

$value =
    trim($_POST["value"] ?? "");


if ($value === "") {

    echo json_encode([
        "success" => false,
        "error" => "Input cannot be empty."
    ]);

    exit;
}


/* =========================
   PASSWORD ANALYZER
========================= */

function analyzePassword($password) {

    $score = 0;

    $signals = [];

    $tips = [];


    $length =
        strlen($password);


    /* LENGTH */

    if ($length >= 16) {

        $score += 30;

        $signals[] = [
            "label" => "Password length",
            "detail" => "Excellent"
        ];

    }

    elseif ($length >= 12) {

        $score += 25;

        $signals[] = [
            "label" => "Password length",
            "detail" => "Good"
        ];

    }

    elseif ($length >= 8) {

        $score += 15;

        $signals[] = [
            "label" => "Password length",
            "detail" => "Medium"
        ];

        $tips[] =
            "Use at least 12-16 characters.";

    }

    else {

        $score += 5;

        $signals[] = [
            "label" => "Password length",
            "detail" => "Too short"
        ];

        $tips[] =
            "Increase the password length.";
    }


    /* UPPERCASE */

    if (preg_match('/[A-Z]/', $password)) {

        $score += 10;

        $signals[] = [
            "label" => "Uppercase letters",
            "detail" => "Detected"
        ];

    } else {

        $signals[] = [
            "label" => "Uppercase letters",
            "detail" => "Missing"
        ];

        $tips[] =
            "Add uppercase letters.";
    }


    /* LOWERCASE */

    if (preg_match('/[a-z]/', $password)) {

        $score += 10;

        $signals[] = [
            "label" => "Lowercase letters",
            "detail" => "Detected"
        ];

    } else {

        $signals[] = [
            "label" => "Lowercase letters",
            "detail" => "Missing"
        ];

        $tips[] =
            "Add lowercase letters.";
    }


    /* NUMBERS */

    if (preg_match('/[0-9]/', $password)) {

        $score += 10;

        $signals[] = [
            "label" => "Numbers",
            "detail" => "Detected"
        ];

    } else {

        $signals[] = [
            "label" => "Numbers",
            "detail" => "Missing"
        ];

        $tips[] =
            "Add numbers.";
    }


    /* SPECIAL */

    if (preg_match('/[^A-Za-z0-9]/', $password)) {

        $score += 15;

        $signals[] = [
            "label" => "Special characters",
            "detail" => "Detected"
        ];

    } else {

        $signals[] = [
            "label" => "Special characters",
            "detail" => "Missing"
        ];

        $tips[] =
            "Add special characters.";
    }


    /* REPEATED */

    if (preg_match('/(.)\1{2,}/', $password)) {

        $score -= 15;

        $signals[] = [
            "label" => "Repeated characters",
            "detail" => "Weak pattern detected"
        ];

        $tips[] =
            "Avoid repeated characters.";

    } else {

        $score += 5;

        $signals[] = [
            "label" => "Repeated characters",
            "detail" => "No obvious repetition"
        ];
    }


    /* SEQUENCE */

    if (preg_match(
        '/(123|234|345|456|567|678|789|abc|bcd|cde|qwe|asd)/i',
        $password
    )) {

        $score -= 15;

        $signals[] = [
            "label" => "Sequential pattern",
            "detail" => "Detected"
        ];

        $tips[] =
            "Avoid predictable sequences.";

    } else {

        $score += 5;

        $signals[] = [
            "label" => "Sequential pattern",
            "detail" => "Not detected"
        ];
    }


    /* COMMON PASSWORD */

    $common = [

        "password",
        "password123",
        "123456",
        "12345678",
        "123456789",
        "qwerty",
        "qwerty123",
        "admin",
        "admin123",
        "letmein",
        "welcome",
        "iloveyou",
        "abc123"
    ];


    if (
        in_array(
            strtolower($password),
            $common,
            true
        )
    ) {

        $score = 5;

        $signals[] = [
            "label" => "Common password",
            "detail" => "Highly predictable"
        ];

        $tips[] =
            "Never use common passwords.";

    } else {

        $signals[] = [
            "label" => "Common password",
            "detail" => "Not detected"
        ];
    }


    $score =
        max(0, min(100, $score));


    if ($score >= 75) {

        $verdict = "SAFE";

        $title = "Strong Password";

        $why =
            "This password has good length and complexity with no major predictable pattern detected.";

    }

    elseif ($score >= 50) {

        $verdict = "SUSPICIOUS";

        $title = "Medium Password";

        $why =
            "This password has some security weaknesses and should be strengthened.";

    }

    else {

        $verdict = "DANGEROUS";

        $title = "Weak Password";

        $why =
            "This password contains characteristics that make it easier to guess or crack.";
    }


    return [

        "success" => true,

        "verdict" => $verdict,

        "score" => $score,

        "title" => $title,

        "why" => $why,

        "signals" => $signals,

        "tips" => array_slice(
            array_unique($tips),
            0,
            5
        )

    ];
}


/* =========================
   MESSAGE ANALYZER
========================= */

function analyzeMessage($message) {

    $text =
        strtolower($message);

    $score = 0;

    $signals = [];

    $tips = [];


    $phishingWords = [

        "verify your account",
        "verify account",
        "account suspended",
        "account blocked",
        "click here",
        "login immediately",
        "confirm your identity",
        "update your account",
        "reset your password",
        "your account will be closed"

    ];


    $urgencyWords = [

        "urgent",
        "immediately",
        "act now",
        "within 24 hours",
        "last warning",
        "final warning",
        "as soon as possible"

    ];


    $moneyWords = [

        "payment",
        "money",
        "transfer",
        "bank",
        "refund",
        "prize",
        "lottery",
        "reward",
        "cash"

    ];


    $credentialWords = [

        "password",
        "otp",
        "pin",
        "cvv",
        "card number",
        "login",
        "username"

    ];


    $phishingFound = [];

    foreach ($phishingWords as $word) {

        if (strpos($text, $word) !== false) {

            $phishingFound[] = $word;

        }

    }


    if (count($phishingFound) > 0) {

        $score +=
            min(35, count($phishingFound) * 15);

        $signals[] = [
            "label" => "Phishing language",
            "detail" => "Detected"
        ];

        $tips[] =
            "Do not click links in suspicious messages.";

    } else {

        $signals[] = [
            "label" => "Phishing language",
            "detail" => "Not detected"
        ];
    }


    $urgencyFound = 0;

    foreach ($urgencyWords as $word) {

        if (strpos($text, $word) !== false) {

            $urgencyFound++;

        }

    }


    if ($urgencyFound > 0) {

        $score += 20;

        $signals[] = [
            "label" => "Urgency pressure",
            "detail" => "Detected"
        ];

        $tips[] =
            "Do not act immediately because of pressure.";

    } else {

        $signals[] = [
            "label" => "Urgency pressure",
            "detail" => "Low"
        ];
    }


    $credentialFound = 0;

    foreach ($credentialWords as $word) {

        if (strpos($text, $word) !== false) {

            $credentialFound++;

        }

    }


    if ($credentialFound > 0) {

        $score += 25;

        $signals[] = [
            "label" => "Credential request",
            "detail" => "Detected"
        ];

        $tips[] =
            "Never share passwords, OTPs or PINs.";

    } else {

        $signals[] = [
            "label" => "Credential request",
            "detail" => "Not detected"
        ];
    }


    $moneyFound = 0;

    foreach ($moneyWords as $word) {

        if (strpos($text, $word) !== false) {

            $moneyFound++;

        }

    }


    if ($moneyFound > 0) {

        $score += 15;

        $signals[] = [
            "label" => "Financial language",
            "detail" => "Detected"
        ];

    } else {

        $signals[] = [
            "label" => "Financial language",
            "detail" => "Not detected"
        ];
    }


    /* URL INSIDE MESSAGE */

    if (
        preg_match(
            '/https?:\/\/[^\s]+/i',
            $message
        )
    ) {

        $score += 20;

        $signals[] = [
            "label" => "Link in message",
            "detail" => "Detected"
        ];

        $tips[] =
            "Verify the website independently.";

    } else {

        $signals[] = [
            "label" => "Link in message",
            "detail" => "None detected"
        ];
    }


    $score =
        max(0, min(100, $score));


    if ($score >= 60) {

        $verdict = "DANGEROUS";

        $title = "Likely Phishing / Scam";

        $why =
            "The message contains multiple characteristics commonly associated with phishing or scam attempts.";

    }

    elseif ($score >= 30) {

        $verdict = "SUSPICIOUS";

        $title = "Suspicious Message";

        $why =
            "The message contains some warning signs that require additional verification.";

    }

    else {

        $verdict = "SAFE";

        $title = "No Major Threat Detected";

        $why =
            "No strong phishing or scam indicators were detected by the current security rules.";
    }


    return [

        "success" => true,

        "verdict" => $verdict,

        "score" => $score,

        "title" => $title,

        "why" => $why,

        "signals" => $signals,

        "tips" => array_slice(
            array_unique($tips),
            0,
            5
        )

    ];
}


/* =========================
   URL ANALYZER
========================= */

function analyzeURL($url) {

    $score = 0;

    $signals = [];

    $tips = [];


    $parsed =
        parse_url($url);


    /* HTTPS */

    if (
        isset($parsed["scheme"]) &&
        strtolower($parsed["scheme"]) === "https"
    ) {

        $signals[] = [
            "label" => "HTTPS",
            "detail" => "Enabled"
        ];

    } else {

        $score += 20;

        $signals[] = [
            "label" => "HTTPS",
            "detail" => "Missing"
        ];

        $tips[] =
            "Prefer HTTPS websites.";
    }


    /* DOMAIN */

    $host =
        $parsed["host"] ?? "";


    if ($host === "") {

        return [

            "success" => true,

            "verdict" => "DANGEROUS",

            "score" => 90,

            "title" => "Invalid URL",

            "why" =>
                "The provided text does not contain a valid website domain.",

            "signals" => [[

                "label" => "Domain",
                "detail" => "Invalid"

            ]],

            "tips" => [

                "Enter a complete website URL."

            ]

        ];

    }


    /* IP ADDRESS */

    if (
        filter_var(
            $host,
            FILTER_VALIDATE_IP
        )
    ) {

        $score += 30;

        $signals[] = [
            "label" => "IP address",
            "detail" => "Used instead of domain"
        ];

        $tips[] =
            "Be careful with login pages using raw IP addresses.";

    } else {

        $signals[] = [
            "label" => "IP address",
            "detail" => "Not detected"
        ];
    }


    /* @ SYMBOL */

    if (strpos($url, "@") !== false) {

        $score += 25;

        $signals[] = [
            "label" => "@ character",
            "detail" => "Suspicious"
        ];

        $tips[] =
            "Avoid URLs containing unexpected @ symbols.";

    } else {

        $signals[] = [
            "label" => "@ character",
            "detail" => "Not detected"
        ];
    }


    /* LENGTH */

    $length =
        strlen($url);


    if ($length > 150) {

        $score += 15;

        $signals[] = [
            "label" => "URL length",
            "detail" => "Very long"
        ];

    }

    elseif ($length > 100) {

        $score += 8;

        $signals[] = [
            "label" => "URL length",
            "detail" => "Long"
        ];

    }

    else {

        $signals[] = [
            "label" => "URL length",
            "detail" => "Normal"
        ];
    }


    /* SUBDOMAINS */

    $parts =
        explode(".", $host);


    if (count($parts) >= 4) {

        $score += 15;

        $signals[] = [
            "label" => "Subdomains",
            "detail" => "Excessive"
        ];

        $tips[] =
            "Check the actual registered domain carefully.";

    } else {

        $signals[] = [
            "label" => "Subdomains",
            "detail" => "Normal"
        ];
    }


    /* SUSPICIOUS KEYWORDS */

    $keywords = [

        "login",
        "verify",
        "secure",
        "account",
        "update",
        "password",
        "confirm",
        "wallet",
        "bank"

    ];


    $found = [];

    foreach ($keywords as $keyword) {

        if (
            stripos(
                $url,
                $keyword
            ) !== false
        ) {

            $found[] = $keyword;

        }

    }


    if (count($found) >= 2) {

        $score += 15;

        $signals[] = [
            "label" => "Suspicious keywords",
            "detail" => "Multiple detected"
        ];

    } else {

        $signals[] = [
            "label" => "Suspicious keywords",
            "detail" => "Low"
        ];
    }


    /* PUNYCODE */

    if (
        stripos(
            $host,
            "xn--"
        ) !== false
    ) {

        $score += 30;

        $signals[] = [
            "label" => "Punycode domain",
            "detail" => "Detected"
        ];

        $tips[] =
            "Be careful with look-alike internationalized domains.";

    } else {

        $signals[] = [
            "label" => "Punycode domain",
            "detail" => "Not detected"
        ];
    }


    $score =
        max(0, min(100, $score));


    if ($score >= 60) {

        $verdict = "DANGEROUS";

        $title = "High-Risk URL";

        $why =
            "The URL contains multiple structural indicators commonly associated with suspicious or phishing links.";

    }

    elseif ($score >= 30) {

        $verdict = "SUSPICIOUS";

        $title = "Suspicious URL";

        $why =
            "The URL contains some warning signs. Verify the domain before opening it.";

    }

    else {

        $verdict = "SAFE";

        $title = "No Major Risk Detected";

        $why =
            "No major suspicious URL patterns were detected by the current rules.";
    }


    return [

        "success" => true,

        "verdict" => $verdict,

        "score" => $score,

        "title" => $title,

        "why" => $why,

        "signals" => $signals,

        "tips" => array_slice(
            array_unique($tips),
            0,
            5
        )

    ];
}


/* =========================
   ROUTER
========================= */

switch ($type) {

    case "password":

        $result =
            analyzePassword($value);

        break;


    case "message":

        $result =
            analyzeMessage($value);

        break;


    case "url":

        $result =
            analyzeURL($value);

        break;


    default:

        $result = [

            "success" => false,

            "error" =>
                "Invalid analyzer type."

        ];

}


echo json_encode(
    $result,
    JSON_UNESCAPED_SLASHES
);
?>