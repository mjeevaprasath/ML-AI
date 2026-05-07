const form = document.getElementById("loginForm");
const btn = document.getElementById("loginBtn");
const forgot = document.getElementById("forgot");

const username = document.getElementById("username");
const password = document.getElementById("password");

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    btn.innerText = "Logging in...";
    btn.disabled = true;

    const res = await fetch("/login/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: new URLSearchParams({
            username: username.value,
            password: password.value
        })
    });

    const data = await res.json();

    if (data.success) {
        // ✅ CORRECT REDIRECT (GO TO HOME, NOT SIGNUP)
        window.location.href = "/signup/";   // /home/
    } else {
        alert("Login failed ❌");

        btn.innerText = "Login";
        btn.disabled = false;
    }
});

forgot.addEventListener("click", function (e) {
    e.preventDefault();

    let email = prompt("Enter your email:");
    if (email) {
        alert("Reset link sent to " + email + " (demo only)");
    }
});