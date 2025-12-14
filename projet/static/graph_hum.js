let humChart;

async function loadHumGraph() {
    try {
        const res = await fetch('/api/');
        const data = await res.json();

        // Vérifier que le canvas existe
        const canvas = document.getElementById('humChart');
        if (!canvas) {
            console.error("Le canvas #humChart n'existe pas !");
            return;
        }
        const ctx = canvas.getContext('2d');

        // Filtrer les mesures valides
        const validData = data.filter(d => d.humidity !== null && d.timestamp);
        if (!validData.length) {
            console.warn("Aucune donnée valide pour l'humidité !");
            return;
        }

        // Transformer les timestamps pour JS
        const labels = validData.map(d => {
            let ts = d.timestamp.replace(/\.\d+/, '').replace('+00:00', 'Z');
            return new Date(ts).toLocaleTimeString();
        });

        const values = validData.map(d => d.humidity);

        console.log("Labels:", labels, "Values:", values); // debug

        if (humChart) {
            // Mise à jour du graphique existant
            humChart.data.labels = labels;
            humChart.data.datasets[0].data = values;
            humChart.update();
        } else {
            // Création du graphique
            humChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Humidité (%)',
                        data: values,
                        borderColor: 'rgb(54, 162, 235)',
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        tension: 0.3,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { suggestedMin: 0, suggestedMax: 100 },
                        x: { title: { display: true, text: 'Heure' } }
                    },
                    plugins: {
                        legend: { display: true },
                        tooltip: { mode: 'index', intersect: false }
                    }
                }
            });
        }

    } catch (err) {
        console.error("Erreur fetch hum:", err);
    }
}

// ⚡ Attendre que la page soit chargée
document.addEventListener("DOMContentLoaded", () => {
    loadHumGraph();
    setInterval(loadHumGraph, 5000);
});
