<?php

function analyzeURL(string $url): array
{

    $patterns =
        require __DIR__ .
        "/../data/suspicious_patterns.php";


    $score = 0;

    $signals = [];

    $tips = [];


    $original =
        trim($url);


    $parseURL =
        $original;


    if (
        !preg_match(
            "/^[a-z][a-z0-9+\-.]*:\/\//i",
            $parseURL
        )
    ) {

        $parseURL =
            "https://" .
            $parseURL;

    }


    $parts =
        parse_url(
            $parseURL
        );


    if (
        $parts === false ||
        empty($parts["host"])
    ) {

        return [

            "success" => true,

            "type" => "url",

            "verdict" =>
                "DANGEROUS",

            "score" =>
                0,

            "title" =>
                "Invalid URL",

            "why" =>
                "The supplied text could not be parsed as a valid website URL.",

            "signals" => [

                [

                    "label" =>
                        "URL format",

                    "level" =>
                        "bad",

                    "detail" =>
                        "Invalid"

                ]

            ],

            "tips" => [

                "Enter a valid URL such as https://example.com."

            ]

        ];

    }


    $host =
        strtolower(
            $parts["host"]
        );


    $full =
        strtolower(
            $parseURL
        );


    /* HTTPS */

    $scheme =
        strtolower(
            $parts["scheme"] ?? ""
        );


    if (
        $scheme === "https"
    ) {

        $signals[] = [

            "label" =>
                "HTTPS encryption",

            "level" =>
                "good",

            "detail" =>
                "HTTPS detected"

        ];

    }

    else {

        $score += 12;


        $signals[] = [

            "label" =>
                "HTTPS encryption",

            "level" =>
                "warning",

            "detail" =>
                "HTTP / no HTTPS"

        ];


        $tips[] =
            "Prefer HTTPS websites.";

    }


    /* IP */

    if (
        filter_var(
            $host,
            FILTER_VALIDATE_IP
        )
    ) {

        $score += 25;


        $signals[] = [

            "label" =>
                "IP address host",

            "level" =>
                "bad",

            "detail" =>
                $host

        ];


        $tips[] =
            "Be cautious with URLs using a raw IP address.";

    }

    else {

        $signals[] = [

            "label" =>
                "Domain host",

            "level" =>
                "good",

            "detail" =>
                $host

        ];

    }


    /* @ SYMBOL */

    if (
        strpos(
            $full,
            "@"
        ) !== false
    ) {

        $score += 25;


        $signals[] = [

            "label" =>
                "At-symbol trick",

            "level" =>
                "bad",

            "detail" =>
                "@ detected"

        ];


        $tips[] =
            "Do not trust URLs that use @ to hide the actual destination.";

    }


    /* PUNYCODE */

    if (
        strpos(
            $host,
            "xn--"
        ) !== false
    ) {

        $score += 25;


        $signals[] = [

            "label" =>
                "Punycode domain",

            "level" =>
                "bad",

            "detail" =>
                "xn-- detected"

        ];


        $tips[] =
            "Check internationalized domains carefully.";

    }


    /* SHORTENER */

    foreach (
        $patterns["url_shorteners"]
        as $shortener
    ) {

        if (
            $host === $shortener ||
            str_ends_with(
                $host,
                "." . $shortener
            )
        ) {

            $score += 15;


            $signals[] = [

                "label" =>
                    "URL shortener",

                "level" =>
                    "warning",

                "detail" =>
                    $shortener

            ];


            $tips[] =
                "Verify the final destination of shortened links.";

            break;

        }

    }


    /* SUSPICIOUS TLD */

    foreach (
        $patterns["suspicious_tlds"]
        as $tld
    ) {

        if (
            str_ends_with(
                $host,
                $tld
            )
        ) {

            $score += 10;


            $signals[] = [

                "label" =>
                    "Unusual domain ending",

                "level" =>
                    "warning",

                "detail" =>
                    $tld

            ];

            break;

        }

    }


    /* SUBDOMAINS */

    $labels =
        explode(
            ".",
            $host
        );


    if (
        count($labels) >= 5
    ) {

        $score += 12;


        $signals[] = [

            "label" =>
                "Many subdomains",

            "level" =>
                "warning",

            "detail" =>
                count($labels) .
                " labels"

        ];


        $tips[] =
            "Check the actual registered domain.";

    }

    else {

        $signals[] = [

            "label" =>
                "Subdomain structure",

            "level" =>
                "good",

            "detail" =>
                "Normal"

        ];

    }


    /* LENGTH */

    if (
        strlen($original) > 180
    ) {

        $score += 10;


        $signals[] = [

            "label" =>
                "URL length",

            "level" =>
                "warning",

            "detail" =>
                strlen($original) .
                " characters"

        ];

    }

    else {

        $signals[] = [

            "label" =>
                "URL length",

            "level" =>
                "good",

            "detail" =>
                strlen($original) .
                " characters"

        ];

    }


    /* SUSPICIOUS WORDS */

    $hits = [];


    foreach (
        $patterns["suspicious_url_words"]
        as $word
    ) {

        if (
            strpos(
                $full,
                $word
            ) !== false
        ) {

            $hits[] =
                $word;

        }

    }


    if (
        count($hits) > 0
    ) {

        $score += min(
            18,
            count($hits) * 5
        );


        $signals[] = [

            "label" =>
                "Suspicious URL words",

            "level" =>
                "warning",

            "detail" =>
                count($hits) .
                " detected"

        ];


        $tips[] =
            "Verify that the domain is the official website.";

    }

    else {

        $signals[] = [

            "label" =>
                "Suspicious URL words",

            "level" =>
                "good",

            "detail" =>
                "Not detected"

        ];

    }


    /* ENCODED CHARACTERS */

    if (
        preg_match(
            "/%[0-9a-f]{2}/i",
            $original
        )
    ) {

        $score += 5;


        $signals[] = [

            "label" =>
                "Encoded characters",

            "level" =>
                "warning",

            "detail" =>
                "Detected"

        ];

    }


    /* HYPHENS */

    if (
        substr_count(
            $host,
            "-"
        ) >= 3
    ) {

        $score += 7;


        $signals[] = [

            "label" =>
                "Domain hyphens",

            "level" =>
                "warning",

            "detail" =>
                "Multiple hyphens"

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

    if (
        $score >= 55
    ) {

        $verdict =
            "DANGEROUS";

        $title =
            "High-Risk URL";

        $why =
            "Several structural indicators associated with suspicious or deceptive URLs were detected.";

    }

    elseif (
        $score >= 25
    ) {

        $verdict =
            "SUSPICIOUS";

        $title =
            "Suspicious URL";

        $why =
            "The URL contains indicators that should be verified before visiting or entering sensitive information.";

    }

    else {

        $verdict =
            "SAFE";

        $title =
            "No Major URL Threat Indicators";

        $why =
            "The URL structure does not contain major indicators covered by the current rules. Static analysis cannot guarantee that a website is legitimate.";

    }


    if (
        count($tips) === 0
    ) {

        $tips[] =
            "Verify the domain before entering sensitive information.";

    }


    return [

        "success" => true,

        "type" => "url",

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