async function loadLatest() {
    try {
        const res = await fetch("/latest/");
        const data = await res.json();

        document.getElementById("temp-value").textContent = data.temperature + " °C";
        document.getElementById("hum-value").textContent = data.humidity + " %";

        const date = new Date(data.timestamp);
        const diffSec = Math.round((Date.now() - date) / 1000);

        const formattedTime = `il y a ${diffSec} secondes (à ${date.toLocaleTimeString()})`;
        document.getElementById("temp-time").textContent = formattedTime;
        document.getElementById("hum-time").textContent = formattedTime;

    } catch (e) {
        console.log("Erreur API :", e);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    loadLatest();
    setInterval(loadLatest, 5000);
});
