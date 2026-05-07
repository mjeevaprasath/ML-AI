document.addEventListener("DOMContentLoaded", function () {

    console.log("LENS JS LOADED 🚀");

    const input = document.getElementById("searchInput");
    const btn = document.getElementById("voiceBtn");
    const results = document.getElementById("results");

    let isTyping = false;

    // 🔄 ICON CHANGE
    input.addEventListener("input", () => {
        if (!isTyping) {
            btn.innerText = input.value.trim() !== "" ? "⬆️" : "🎤";
        }
    });

    // 🔍 ENTER KEY
    input.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
            e.preventDefault();
            sendLens();
        }
    });

    // 🔥 BUTTON CLICK
    btn.addEventListener("click", function () {

        if (isTyping) {
            isTyping = false;
            btn.innerText = "⬆️";
            return;
        }

        if (input.value.trim() !== "") {
            sendLens();
        }
    });

    // 🚀 MAIN FUNCTION
    function sendLens() {

        const query = input.value.trim();
        if (!query) return;

        console.log("SENDING:", query);

        document.querySelector(".search-box").classList.add("active");

        results.innerHTML = "Thinking... 🤖";

        isTyping = true;
        btn.innerText = "🚫";

        fetch("/lens_api/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ query: query })
        })
        .then(res => res.json())
        .then(data => {

            console.log("FULL RESPONSE:", data);

            results.innerHTML = "";

            let div = document.createElement("div");
            div.className = "result";
            results.appendChild(div);

            let answer = data.response;

            // 🛑 SAFETY CHECK
            if (!answer) {
                div.innerHTML = "No response 😕";
                isTyping = false;
                btn.innerText = "⬆️";
                return;
            }

            // 🔥 FORMAT TEXT
            let formatted = answer
                .replace(/\n/g, "<br><br>")
                .replace(/\*\*(.*?)\*\*/g, "<b>$1</b>");

            let i = 0;

            // ✨ SAFE TYPING FUNCTION
            function typing() {

                // 🛑 STOP IF INTERRUPTED
                if (!isTyping) return;

                // 🔥 AUTO SCROLL
                results.scrollTo({
                    top: results.scrollHeight,
                    behavior: "smooth"
                });

                // 🛑 FINISH CONDITION
                if (i >= formatted.length) {
                    isTyping = false;
                    btn.innerText = "⬆️";
                    return;
                }

                // 🔥 HANDLE HTML TAGS SAFELY
                if (formatted.substring(i, i + 4) === "<br>") {
                    div.innerHTML += "<br>";
                    i += 4;
                }
                else if (formatted.substring(i, i + 3) === "<b>") {
                    div.innerHTML += "<b>";
                    i += 3;
                }
                else if (formatted.substring(i, i + 4) === "</b>") {
                    div.innerHTML += "</b>";
                    i += 4;
                }
                else {
                    div.innerHTML += formatted.charAt(i);
                    i++;
                }

                setTimeout(typing, 10);
            }

            typing();

            input.value = "";
        })
        .catch(err => {
            console.log("ERROR:", err);
            results.innerHTML = "Error 😕";
            isTyping = false;
            btn.innerText = "⬆️";
        });
    }

});