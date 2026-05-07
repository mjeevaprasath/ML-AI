const form = document.getElementById("signupForm");
const btn = document.getElementById("signupBtn");

form.addEventListener("submit", async function(e) {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    // Loading effect
    btn.innerText = "Creating...";
    btn.disabled = true;

    // -------------------
    // FRONTEND VALIDATION
    // -------------------

    if(!email.endsWith("@gmail.com")) {
        alert("Enter valid Gmail ❌");
        return resetBtn();
    }

    if(password.length < 6) {
        alert("Password must be at least 6 characters ❌");
        return resetBtn();
    }

    if(password !== confirmPassword) {
        alert("Passwords do not match ❌");
        return resetBtn();
    }

    // -------------------
    // BACKEND CALL (DJANGO)
    // -------------------

    try {
        const res = await fetch("/signup/", {
            method: "POST",
            headers: {
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: new URLSearchParams({
                username: username,
                email: email,
                password: password,
                confirm_password: confirmPassword
            })
        });

        const data = await res.json();

        if(data.success){
            alert("Account Created Successfully ✅");

            // Redirect to login page
            window.location.href = data.redirect;   // "/login/"
        } else {
            alert(data.error || "Signup failed ❌");
            resetBtn();
        }

    } catch (err) {
        alert("Server error ❌");
        resetBtn();
    }
});

function resetBtn() {
    btn.innerText = "Sign Up";
    btn.disabled = false;
}