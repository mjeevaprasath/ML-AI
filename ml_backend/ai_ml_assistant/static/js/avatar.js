// ----------------------
// 🎭 AVATAR SYSTEM (FIXED)
// ----------------------

window.addEventListener("load", () => {

    const container = document.getElementById("avatar-container");

    let modelRef = null; // ✅ FIX

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x222222);

    const camera = new THREE.PerspectiveCamera(
        75,
        container.clientWidth / container.clientHeight,
        0.1,
        1000
    );
    camera.position.set(0, 1.5, 5);

    const renderer = new THREE.WebGLRenderer({ alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);

    const light = new THREE.DirectionalLight(0xffffff, 3);
    light.position.set(0, 5, 5);
    scene.add(light);

    const ambient = new THREE.AmbientLight(0xffffff, 2);
    scene.add(ambient);

    const loader = new THREE.GLTFLoader();

    loader.load(
        "/static/model/Astronaut.glb",

        (gltf) => {
            console.log("✅ Avatar loaded");

            modelRef = gltf.scene; // ✅ FIX

            modelRef.scale.set(2.5, 2.5, 2.5);
            modelRef.position.set(0, -1.2, 0);
            modelRef.rotation.y = Math.PI;

            scene.add(modelRef);
        },

        undefined,

        (error) => {
            console.error("❌ Avatar load error:", error);
        }
    );

    function animate() {
        requestAnimationFrame(animate);

        if (modelRef) {
            modelRef.rotation.y += 0.01; // ✅ SAFE
        }

        renderer.render(scene, camera);
    }

    animate();
});