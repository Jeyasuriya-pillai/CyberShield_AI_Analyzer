<?php

function analyzeMessage(string $message): array
{

    $data =
        require __DIR__ .
        "/../data/phishing_keywords.php";


    $text =
        strtolower($message);


    $score = 0;

    $signals = [];

    $tips = [];


    /* PHISHING */

    $phishingHits = [];

    foreach (
        $data["phishing"]
        as $word
    ) {

        if (
            stripos(
                $text,
                $word
            ) !== false
        ) {

            $phishingHits[] =
                $word;

        }

    }


    if (
        count($phishingHits) > 0
    ) {

        $score += min(
            30,
            count($phishingHits) * 10
        );


        $signals[] = [

            "label" =>
                "Phishing language",

            "level" =>
                "bad",

            "detail" =>
                count($phishingHits) .
                " indicator(s)"

        ];


        $tips[] =
            "Do not click links or follow unexpected verification instructions.";

    }

    else {

        $signals[] = [

            "label" =>
                "Phishing language",

            "level" =>
                "good",

            "detail" =>
                "Not detected"

        ];

    }


    /* URGENCY */

    $urgencyHits = [];


    foreach (
        $data["urgency"]
        as $word
    ) {

        if (
            stripos(
                $text,
                $word
            ) !== false
        ) {

            $urgencyHits[] =
                $word;

        }

    }


    if (
        count($urgencyHits) > 0
    ) {

        $score += min(
            20,
            count($urgencyHits) * 7
        );


        $signals[] = [

            "label" =>
                "Urgency pressure",

            "level" =>
                "warning",

            "detail" =>
                count($urgencyHits) .
                " indicator(s)"

        ];


        $tips[] =
            "Be careful when a message pressures you to act immediately.";

    }

    else {

        $signals[] = [

            "label" =>
                "Urgency pressure",

            "level" =>
                "good",

            "detail" =>
                "Low"

        ];

    }


    /* CREDENTIALS */

    $credentialHits = [];


    foreach (
        $data["credentials"]
        as $word
    ) {

        if (
            stripos(
                $text,
                $word
            ) !== false
        ) {

            $credentialHits[] =
                $word;

        }

    }


    if (
        count($credentialHits) > 0
    ) {

        $score += min(
            25,
            count($credentialHits) * 8
        );


        $signals[] = [

            "label" =>
                "Credential request",

            "level" =>
                "bad",

            "detail" =>
                count($credentialHits) .
                " indicator(s)"

        ];


        $tips[] =
            "Never share passwords, OTPs, PINs or CVVs through unexpected messages.";

    }

    else {

        $signals[] = [

            "label" =>
                "Credential request",

            "level" =>
                "good",

            "detail" =>
                "Not detected"

        ];

    }


    /* FINANCIAL */

    $financialHits = [];


    foreach (
        $data["financial"]
        as $word
    ) {

        if (
            stripos(
                $text,
                $word
            ) !== false
        ) {

            $financialHits[] =
                $word;

        }

    }


    if (
        count($financialHits) > 0
    ) {

        $score += min(
            20,
            count($financialHits) * 5
        );


        $signals[] = [

            "label" =>
                "Financial/scam terms",

            "level" =>
                "warning",

            "detail" =>
                count($financialHits) .
                " indicator(s)"

        ];


        $tips[] =
            "Verify financial claims using the official website or app.";

    }

    else {

        $signals[] = [

            "label" =>
                "Financial/scam terms",

            "level" =>
                "good",

            "detail" =>
                "Not detected"

        ];

    }


    /* THREATS */

    $threatHits = [];


    foreach (
        $data["threats"]
        as $word
    ) {

        if (
            stripos(
                $text,
                $word
            ) !== false
        ) {

            $threatHits[] =
                $word;

        }

    }


    if (
        count($threatHits) > 0
    ) {

        $score += min(
            15,
            count($threatHits) * 7
        );


        $signals[] = [

            "label" =>
                "Threatening language",

            "level" =>
                "bad",

            "detail" =>
                count($threatHits) .
                " indicator(s)"

        ];


        $tips[] =
            "Do not respond to threats by sending money or personal information.";

    }

    else {

        $signals[] = [

            "label" =>
                "Threatening language",

            "level" =>
                "good",

            "detail" =>
                "Not detected"

        ];

    }


    /* URL */

    if (
        preg_match(
            "/https?:\/\/[^\s]+|www\.[^\s]+/i",
            $message
        )
    ) {

        $score += 10;


        $signals[] = [

            "label" =>
                "Link detected",

            "level" =>
                "warning",

            "detail" =>
                "URL found"

        ];


        $tips[] =
            "Check the destination domain before opening the link.";

    }

    else {

        $signals[] = [

            "label" =>
                "Link detection",

            "level" =>
                "good",

            "detail" =>
                "No URL found"

        ];

    }


    $score =
        max(
            0,
            min(
                100,
                $score
            )
        );


    /* VERDICT */

    if ($score >= 60) {

        $verdict =
            "DANGEROUS";

        $title =
            "Likely Phishing / Scam";

        $why =
            "Multiple suspicious indicators were detected. Treat this message as potentially malicious.";

    }

    elseif ($score >= 30) {

        $verdict =
            "SUSPICIOUS";

        $title =
            "Suspicious Message";

        $why =
            "The message contains warning signs that should be verified before taking action.";

    }

    else {

        $verdict =
            "SAFE";

        $title =
            "No Major Threat Indicators";

        $why =
            "The current rules did not find major phishing or scam indicators. This does not guarantee that the message is legitimate.";

    }


    if (
        count($tips) === 0
    ) {

        $tips[] =
            "Verify the sender and context before trusting the message.";

    }


    return [

        "success" => true,

        "type" => "message",

        "verdict" =>
            $verdict,

        "score" =>
            $score,

        "title" =>
            $title,

        "why" =>
            $why,

        "signals" =>
            $signals,

        "tips" =>
            array_values(
                array_unique($tips)
            )

    ];

}