<?php

header(
    "Content-Type: application/json; charset=UTF-8"
);


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
    trim(
        $_POST["value"] ?? ""
    );


if ($type === "") {

    echo json_encode([
        "success" => false,
        "error" => "Analyzer type is missing."
    ]);

    exit;
}


if ($value === "") {

    echo json_encode([
        "success" => false,
        "error" => "Input cannot be empty."
    ]);

    exit;
}


try {

    require_once
        __DIR__ .
        "/password_analyzer.php";

    require_once
        __DIR__ .
        "/message_analyzer.php";

    require_once
        __DIR__ .
        "/url_analyzer.php";


    switch ($type) {

        case "password":

            $result =
                analyzePassword(
                    $value
                );

            break;


        case "message":

            $result =
                analyzeMessage(
                    $value
                );

            break;


        case "url":

            $result =
                analyzeURL(
                    $value
                );

            break;


        default:

            echo json_encode([
                "success" => false,
                "error" => "Invalid analyzer type."
            ]);

            exit;
    }


    echo json_encode(
        $result,
        JSON_UNESCAPED_UNICODE |
        JSON_UNESCAPED_SLASHES
    );

}

catch (Throwable $e) {

    http_response_code(500);

    echo json_encode([

        "success" => false,

        "error" =>
            "PHP Analyzer Error: " .
            $e->getMessage()

    ]);

}

exit;