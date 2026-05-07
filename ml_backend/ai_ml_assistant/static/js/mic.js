// ----------------------
// 🎤 CHAT + VOICE SYSTEM
// ----------------------

import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { VRMLoaderPlugin } from '@pixiv/three-vrm';

const micBtn = document.getElementById("mic-btn");
const chatBox = document.getElementById("chat-box");

// 🎤 Speech Recognition
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = "en-US";

micBtn.onclick = () => recognition.start();

recognition.onresult = async (event) => {
    const text = event.results[0][0].transcript;

    addMessage("You", text);
    const aiReply = await sendToAI(text);
    addMessage("AI", aiReply);

    speak(aiReply);
};

function addMessage(sender, text) {
    const div = document.createElement("div");
    div.className = "msg";
    div.innerHTML = `<b>${sender}:</b> ${text}`;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendToAI(text) {
    try {
        const res = await fetch("/process/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: text })
        });

        const data = await res.json();
        return data.results[0];
    } catch {
        return "AI error 😢";
    }
}

// ----------------------
// 💋 LIP + EMOTION SYSTEM
// ----------------------

let currentPhonemes = [];
let lipStartTime = 0;
let vrm = null;
let isTalking = false;

let emotionTarget = 0;
let emotionCurrent = 0;

let blinkTimer = 0;
let nextBlink = 2 + Math.random() * 3;

let idleLookTimer = 0;
let idleTargetX = 0;
let idleTargetY = 0;

function resetMouth(vrm) {
    ['aa','ee','ih','oh','ou'].forEach(k => {
        vrm.expressionManager.setValue(k, 0);
    });
}

function applyPhoneme(vrm, phoneme) {
    const map = {
        A:'aa',E:'ee',I:'ih',O:'oh',U:'ou',
        B:'aa',C:'ee',D:'aa',F:'ou',
        G:'ee',H:'oh'
    };

    ['aa','ee','ih','oh','ou'].forEach(k => {
        let v = vrm.expressionManager.getValue(k) || 0;
        vrm.expressionManager.setValue(k, v * 0.6);
    });

    if (map[phoneme]) {
        vrm.expressionManager.setValue(map[phoneme], 1);
    }
}

function updateLipSync(vrm) {
    if (!currentPhonemes.length) {
        resetMouth(vrm);
        isTalking = false;
        return;
    }

    const t = (performance.now() - lipStartTime) / 1000;
    isTalking = true;

    for (let p of currentPhonemes) {
        if (t >= p.time) {
            applyPhoneme(vrm, p.phoneme);
        }
    }
}

// 👁 blink
function updateBlink(vrm, delta) {
    blinkTimer += delta;

    if (blinkTimer > nextBlink) {
        vrm.expressionManager.setValue('blink', 1);
        setTimeout(() => vrm.expressionManager.setValue('blink', 0), 120);

        blinkTimer = 0;
        nextBlink = 2 + Math.random() * 4;
    }
}

// 🎭 emotion
function updateEmotion(vrm) {
    emotionCurrent += (emotionTarget - emotionCurrent) * 0.05;

    vrm.expressionManager.setValue("happy", Math.max(0, emotionCurrent));
    vrm.expressionManager.setValue("angry", Math.max(0, emotionCurrent * 0.6));
    vrm.expressionManager.setValue("sad", Math.max(0, -emotionCurrent));
}

// ----------------------
// 🎧 SPEAK
// ----------------------

async function speak(text) {
    try {
        const res = await fetch(`/speak_api/?text=${encodeURIComponent(text)}`);
        const data = await res.json();

        if (!data.audio) return;

        const audio = new Audio("data:audio/wav;base64," + data.audio);

        currentPhonemes = data.phonemes || [];
        lipStartTime = performance.now();

        if (data.emotion === "happy") emotionTarget = 1;
        else if (data.emotion === "sad") emotionTarget = -0.7;
        else if (data.emotion === "angry") emotionTarget = 0.6;
        else emotionTarget = 0;

        audio.onended = () => {
            currentPhonemes = [];
            isTalking = false;
        };

        audio.play().catch(() => {
            document.body.addEventListener("click", () => audio.play(), { once: true });
        });

    } catch (e) {
        console.error("TTS ERROR:", e);
    }
}

// ----------------------
// 🎭 VRM SYSTEM
// ----------------------

window.addEventListener("load", () => {

    const container = document.getElementById("avatar-container");

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x2c2f33);

    const camera = new THREE.PerspectiveCamera(35, container.clientWidth / container.clientHeight, 0.1, 1000);

    const renderer = new THREE.WebGLRenderer({ antialias: true });

    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.outputEncoding = THREE.sRGBEncoding;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 0.9;

    container.appendChild(renderer.domElement);

    // lights
    scene.add(new THREE.DirectionalLight(0xffffff, 1.5).position.set(1,3,2));
    scene.add(new THREE.DirectionalLight(0xffffff, 0.8).position.set(-2,2,-2));
    scene.add(new THREE.AmbientLight(0xffffff, 0.6));

    const loader = new GLTFLoader();
    loader.register((parser) => new VRMLoaderPlugin(parser));

    let humanoid = null;
    let baseY = 0;

    loader.load("/static/model/anime.vrm?v=FINAL", (gltf) => {

        vrm = gltf.userData.vrm;
        humanoid = vrm.humanoid;

        const model = vrm.scene;
        model.rotation.y = Math.PI;
        model.scale.set(1.6, 1.6, 1.6);

        scene.add(model);

        const box = new THREE.Box3().setFromObject(model);
        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3());

        model.position.sub(center);
        model.position.y += size.y * 0.52;

        baseY = model.position.y;

        camera.position.set(0, 1.7, 3.5);
        camera.lookAt(0, 1.5, 0);
    });

    const clock = new THREE.Clock();

    function animate() {
        requestAnimationFrame(animate);

        const delta = clock.getDelta();
        const t = clock.getElapsedTime();

        if (vrm) {
            vrm.update(delta);

            updateLipSync(vrm);
            updateBlink(vrm, delta);
            updateEmotion(vrm);

            if (humanoid) {

                const spine = humanoid.getNormalizedBoneNode('spine');
                const chest = humanoid.getNormalizedBoneNode('chest');

                const breath = Math.sin(t * 1.5) * 0.02;
                const talkBoost = isTalking ? 0.03 : 0;

                spine.rotation.x = breath + talkBoost;
                chest.rotation.x = -breath - talkBoost;

                // 💖 FIXED ARM POSE
                const lUpper = humanoid.getNormalizedBoneNode('leftUpperArm');
                const rUpper = humanoid.getNormalizedBoneNode('rightUpperArm');
                const lLower = humanoid.getNormalizedBoneNode('leftLowerArm');
                const rLower = humanoid.getNormalizedBoneNode('rightLowerArm');

                const idle = Math.sin(t * 1.2) * 0.04;

                // RESET
                lUpper.rotation.set(0,0,0);
                rUpper.rotation.set(0,0,0);
                lLower.rotation.set(0,0,0);
                rLower.rotation.set(0,0,0);

                // APPLY POSE
                lUpper.rotation.z = Math.PI / 6 + idle;
                rUpper.rotation.z = -Math.PI / 6 - idle;

                lUpper.rotation.x = 0.3;
                rUpper.rotation.x = 0.3;

                lLower.rotation.z = Math.PI / 8;
                rLower.rotation.z = -Math.PI / 8;
            }
        }

        renderer.render(scene, camera);
    }

    animate();

    setTimeout(() => {
        addMessage("AI", "Hello! I'm ready. Tell me something 😊");
        speak("Hello! I'm ready. Tell me something");
    }, 1000);
});