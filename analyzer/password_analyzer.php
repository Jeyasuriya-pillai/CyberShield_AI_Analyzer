<?php

function analyzePassword(string $password): array
{

    $commonPasswords =
        require __DIR__ .
        "/../data/common_passwords.php";


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
            "level" => "good",
            "detail" => "$length characters"
        ];

    }

    elseif ($length >= 12) {

        $score += 25;

        $signals[] = [
            "label" => "Password length",
            "level" => "good",
            "detail" => "$length characters"
        ];

    }

    elseif ($length >= 8) {

        $score += 10;

        $signals[] = [
            "label" => "Password length",
            "level" => "warning",
            "detail" => "$length characters"
        ];

        $tips[] =
            "Increase the password to at least 12 characters.";

    }

    else {

        $signals[] = [
            "label" => "Password length",
            "level" => "bad",
            "detail" => "$length characters"
        ];

        $tips[] =
            "Use at least 12 characters.";

    }


    /* CHARACTER TYPES */

    $upper =
        preg_match(
            "/[A-Z]/",
            $password
        );

    $lower =
        preg_match(
            "/[a-z]/",
            $password
        );

    $number =
        preg_match(
            "/[0-9]/",
            $password
        );

    $special =
        preg_match(
            "/[^A-Za-z0-9]/",
            $password
        );


    $checks = [

        [
            "Uppercase letters",
            $upper,
            "Add uppercase letters."
        ],

        [
            "Lowercase letters",
            $lower,
            "Add lowercase letters."
        ],

        [
            "Numbers",
            $number,
            "Add numbers."
        ],

        [
            "Special characters",
            $special,
            "Add special characters."
        ]

    ];


    foreach (
        $checks as $check
    ) {

        if ($check[1]) {

            $score += 10;

            $signals[] = [
                "label" => $check[0],
                "level" => "good",
                "detail" => "Detected"
            ];

        }

        else {

            $signals[] = [
                "label" => $check[0],
                "level" => "warning",
                "detail" => "Missing"
            ];

            $tips[] =
                $check[2];

        }

    }


    /* COMMON PASSWORD */

    $lowerPassword =
        strtolower($password);


    $commonLower =
        array_map(
            "strtolower",
            $commonPasswords
        );


    if (
        in_array(
            $lowerPassword,
            $commonLower,
            true
        )
    ) {

        $score =
            min(
                $score,
                15
            );


        $signals[] = [
            "label" => "Common password",
            "level" => "bad",
            "detail" => "Known weak password"
        ];


        $tips[] =
            "Avoid common and predictable passwords.";

    }

    else {

        $signals[] = [
            "label" => "Common password",
            "level" => "good",
            "detail" => "No exact match"
        ];

    }


    /* REPEATED CHARACTERS */

    if (
        preg_match(
            "/(.)\1{2,}/",
            $password
        )
    ) {

        $score -= 10;

        $signals[] = [
            "label" => "Repeated characters",
            "level" => "bad",
            "detail" => "Repeated pattern"
        ];

        $tips[] =
            "Avoid repeated characters such as aaa or 111.";

    }


    /* SEQUENCES */

    if (
        preg_match(
            "/1234|2345|3456|4567|5678|6789/i",
            $password
        )
        ||
        preg_match(
            "/abcd|bcde|cdef|defg|efgh/i",
            strtolower($password)
        )
    ) {

        $score -= 10;

        $signals[] = [
            "label" => "Sequential pattern",
            "level" => "bad",
            "detail" => "Predictable sequence"
        ];

        $tips[] =
            "Avoid sequences such as 1234 or abcd.";

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

    if ($score >= 75) {

        $verdict = "SAFE";

        $title =
            "Strong Password";

        $why =
            "The password meets several important strength requirements and no major weak pattern was detected.";

    }

    elseif ($score >= 45) {

        $verdict = "SUSPICIOUS";

        $title =
            "Moderate Password";

        $why =
            "The password has some good characteristics, but it can be strengthened further.";

    }

    else {

        $verdict = "DANGEROUS";

        $title =
            "Weak Password";

        $why =
            "The password contains major weaknesses that make it easier to guess or attack.";

    }


    $tips =
        array_values(
            array_unique($tips)
        );


    return [

        "success" => true,

        "type" => "password",

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
            $tips

    ];

}