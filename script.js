document.addEventListener("DOMContentLoaded", function () {

    console.log("CyberShield JS Loaded");


    const tabs = document.querySelectorAll(".tab");
    const panels = document.querySelectorAll(".panel");

    const result = document.getElementById("result");

    const password =
        document.getElementById("password");

    const message =
        document.getElementById("message");

    const showPassword =
        document.getElementById("showPassword");

    const count =
        document.getElementById("count");

    const passwordButton =
        document.getElementById("passwordButton");

    const messageButton =
        document.getElementById("messageButton");

    const urlButton =
        document.getElementById("urlButton");


    /* =========================
       TAB SWITCHING
    ========================= */

    tabs.forEach(function (tab) {

        tab.addEventListener("click", function () {

            const type =
                tab.getAttribute("data-type");


            tabs.forEach(function (item) {
                item.classList.remove("active");
            });


            panels.forEach(function (panel) {
                panel.classList.remove("active");
            });


            tab.classList.add("active");


            const selectedPanel =
                document.getElementById(
                    type + "Panel"
                );


            if (selectedPanel) {
                selectedPanel.classList.add("active");
            }


            result.innerHTML = "";

        });

    });


    /* =========================
       SHOW / HIDE PASSWORD
    ========================= */

    showPassword.addEventListener(
        "click",
        function () {

            if (password.type === "password") {

                password.type = "text";

                showPassword.textContent = "🙈";

            } else {

                password.type = "password";

                showPassword.textContent = "👁";

            }

        }
    );


    /* =========================
       PASSWORD RULES
    ========================= */

    password.addEventListener(
        "input",
        function () {

            updateRule(
                "length",
                password.value.length >= 12,
                "12+ characters"
            );


            updateRule(
                "upper",
                /[A-Z]/.test(password.value),
                "Uppercase"
            );


            updateRule(
                "lower",
                /[a-z]/.test(password.value),
                "Lowercase"
            );


            updateRule(
                "number",
                /[0-9]/.test(password.value),
                "Number"
            );


            updateRule(
                "special",
                /[^A-Za-z0-9]/.test(password.value),
                "Special character"
            );

        }
    );


    function updateRule(
        id,
        valid,
        label
    ) {

        const element =
            document.getElementById(id);


        element.classList.toggle(
            "good",
            valid
        );


        element.textContent =
            (valid ? "✓ " : "✕ ") + label;

    }


    /* =========================
       MESSAGE COUNTER
    ========================= */

    message.addEventListener(
        "input",
        function () {

            count.textContent =
                message.value.length;

        }
    );


    /* =========================
       BUTTONS
    ========================= */

    passwordButton.addEventListener(
        "click",
        function () {
            analyze("password");
        }
    );


    messageButton.addEventListener(
        "click",
        function () {
            analyze("message");
        }
    );


    urlButton.addEventListener(
        "click",
        function () {
            analyze("url");
        }
    );


    /* =========================
       ANALYZE
    ========================= */

    async function analyze(type) {

        let value = "";


        if (type === "password") {

            value =
                password.value.trim();

        }


        else if (type === "message") {

            value =
                message.value.trim();

        }


        else if (type === "url") {

            value =
                document
                .getElementById("url")
                .value
                .trim();

        }


        if (!value) {

            showError(
                "Please enter something to analyze."
            );

            return;

        }


        let button;


        if (type === "password") {
            button = passwordButton;
        }

        else if (type === "message") {
            button = messageButton;
        }

        else {
            button = urlButton;
        }


        const originalText =
            button.textContent;


        button.disabled = true;

        button.textContent =
            "⏳ Analyzing...";


        result.innerHTML = `
            <div class="result-card loading-card">

                <div class="loading-spinner"></div>

                <div>
                    <strong>
                        Analyzing security...
                    </strong>

                    <p>
                        Please wait.
                    </p>
                </div>

            </div>
        `;


        try {

            /*
             * IMPORTANT:
             * analyzer/index.php is inside
             * the analyzer folder.
             */

            const response =
                await fetch(
                    "./analyzer/index.php",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/x-www-form-urlencoded; charset=UTF-8"
                        },

                        body:
                            "type=" +
                            encodeURIComponent(type) +
                            "&value=" +
                            encodeURIComponent(value)
                    }
                );


            const raw =
                await response.text();


            console.log(
                "PHP STATUS:",
                response.status
            );


            console.log(
                "PHP RESPONSE:",
                raw
            );


            if (!response.ok) {

                throw new Error(
                    "PHP HTTP " +
                    response.status +
                    "\n\n" +
                    raw
                );

            }


            let data;


            try {

                data =
                    JSON.parse(raw);

            }

            catch (error) {

                throw new Error(
                    "PHP did not return JSON.\n\n" +
                    raw
                );

            }


            if (!data.success) {

                throw new Error(
                    data.error ||
                    "PHP analyzer error."
                );

            }


            displayResult(data);

        }


        catch (error) {

            console.error(error);


            showError(
                error.message
            );

        }


        finally {

            button.disabled = false;

            button.textContent =
                originalText;

        }

    }


    /* =========================
       RESULT
    ========================= */

    function displayResult(data) {

        const verdict =
            String(
                data.verdict
            ).toLowerCase();


        let signalsHTML = "";


        if (
            Array.isArray(data.signals)
        ) {

            data.signals.forEach(
                function (signal) {

                    let icon = "⚠";


                    if (
                        signal.level === "good"
                    ) {
                        icon = "✓";
                    }


                    if (
                        signal.level === "bad"
                    ) {
                        icon = "✕";
                    }


                    signalsHTML += `

                        <div class="
                            signal
                            ${escapeHTML(signal.level)}
                        ">

                            <span class="signal-icon">
                                ${icon}
                            </span>

                            <span class="signal-name">
                                ${escapeHTML(signal.label)}
                            </span>

                            <span class="signal-detail">
                                ${escapeHTML(signal.detail)}
                            </span>

                        </div>

                    `;

                }
            );

        }


        let tipsHTML = "";


        if (
            Array.isArray(data.tips)
        ) {

            data.tips.forEach(
                function (tip) {

                    tipsHTML += `
                        <li>
                            ${escapeHTML(tip)}
                        </li>
                    `;

                }
            );

        }


        result.innerHTML = `

            <div class="result-card">

                <div class="result-top">

                    <div
                        class="
                            score-box
                            ${escapeHTML(verdict)}
                        "
                    >

                        <strong>
                            ${Number(data.score) || 0}
                        </strong>

                        <span>
                            /100
                        </span>

                    </div>


                    <div class="result-heading">

                        <div class="result-label">
                            SECURITY RESULT
                        </div>

                        <h2 class="${escapeHTML(verdict)}">
                            ${escapeHTML(data.title)}
                        </h2>

                        <p>
                            Verdict:
                            <strong>
                                ${escapeHTML(data.verdict)}
                            </strong>
                        </p>

                    </div>

                </div>


                <div class="analysis-box">

                    <div class="analysis-title">
                        🛡 Security Analysis
                    </div>

                    <p>
                        ${escapeHTML(data.why)}
                    </p>

                </div>


                <div class="section-title">
                    DETECTION SIGNALS
                </div>


                <div class="signals">
                    ${signalsHTML}
                </div>


                <div class="section-title">
                    RECOMMENDATIONS
                </div>


                <ul class="tips">
                    ${tipsHTML}
                </ul>

            </div>

        `;

    }


    /* =========================
       ERROR
    ========================= */

    function showError(message) {

        result.innerHTML = `

            <div class="result-card error-card">

                <div class="error-icon">
                    ⚠️
                </div>

                <div>

                    <strong>
                        Analyzer Error
                    </strong>

                    <p style="white-space:pre-wrap;">
                        ${escapeHTML(message)}
                    </p>

                </div>

            </div>

        `;

    }


    /* =========================
       SECURITY ESCAPE
    ========================= */

    function escapeHTML(value) {

        return String(value)

            .replaceAll(
                "&",
                "&amp;"
            )

            .replaceAll(
                "<",
                "&lt;"
            )

            .replaceAll(
                ">",
                "&gt;"
            )

            .replaceAll(
                '"',
                "&quot;"
            )

            .replaceAll(
                "'",
                "&#039;"
            );

    }

});