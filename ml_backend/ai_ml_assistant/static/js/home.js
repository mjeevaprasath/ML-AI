const canvas = document.getElementById("bgCanvas");
const ctx = canvas.getContext("2d");

function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
resize();

let stars = [];

for (let i = 0; i < 300; i++) {
    stars.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        size: Math.random() * 2,
        speed: Math.random() * 0.5 + 0.2
    });
}

function animate() {
    // Blue glow background  
    let gradient = ctx.createRadialGradient(  
        canvas.width/2,  
        canvas.height/2,  
        100,  
        canvas.width/2,  
        canvas.height/2,  
        canvas.width  
    );  

    gradient.addColorStop(0, "#001f3f");  
    gradient.addColorStop(1, "black");  

    ctx.fillStyle = gradient;  
    ctx.fillRect(0, 0, canvas.width, canvas.height);  

    // Stars  
    ctx.fillStyle = "white";  

    stars.forEach(s => {  
        ctx.beginPath();  
        ctx.arc(s.x, s.y, s.size, 0, Math.PI * 2);  
        ctx.fill();  

        s.y += s.speed;  

        if (s.y > canvas.height) {  
            s.y = 0;  
            s.x = Math.random() * canvas.width;  
        }  
    });  

    requestAnimationFrame(animate);
}

animate();
window.addEventListener("resize", resize);


function openMic(){
    window.location.href="/mic/"
}

// ==========================================
// 🤖 NEW DJANGO CONNECT LOGIC (ADD THIS)
// ==========================================

/*
async function sendCommand(userText) {
    console.log("Sending command to ML:", userText);
    
    // UI-la status kaata oru alert (Optionally)
    // alert("ML is processing your request...");

    try {
        const response = await fetch("/process/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie('csrftoken') 
            },
            body: JSON.stringify({ command: userText })
        });

        const data = await response.json();

        if (data.status === "success") {
            console.log("ML Response:", data.response);
            alert("🤖 ML Says: " + data.response);
        } else {
            alert("Error: " + data.message);
        }

    } catch (error) {
        console.error("Network Error:", error);
        alert("Server not responding. Check Django Terminal!");
    }
}
*/

// CSRF Token Helper (Must for Django POST requests)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.getElementById("lensBtn").addEventListener("click", () => {
    window.location.href = "/lens/";
});

let btn = document.getElementById("lensBtn");
console.log(btn);

document.addEventListener("DOMContentLoaded", function () {

    let lens = document.getElementById("lensBtn");
    console.log("Lens Button:", lens); // optional debug

    if (lens) {
        lens.addEventListener("click", function () {
            window.location.href = "/lens/";
        });
    }

});