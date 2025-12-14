let tempChart;

async function loadTempGraph() {
    try {
        const res = await fetch('/api/');
        const data = await res.json();

        const canvas = document.getElementById('tempChart');
        if (!canvas) {
            console.error("Le canvas #tempChart n'existe pas !");
            return;
        }
        const ctx = canvas.getContext('2d');

        // Filtrer les mesures valides
        const validData = data.filter(d => d.temperature !== null && d.timestamp);
        if (!validData.length) {
            console.warn("Aucune donnée valide pour la température !");
            return;
        }

        // Transformer les timestamps
        const labels = validData.map(d => {
            let ts = d.timestamp.replace(/\.\d+/, '').replace('+00:00', 'Z');
            return new Date(ts).toLocaleTimeString();
        });

        const values = validData.map(d => d.temperature);

        console.log("Labels:", labels, "Values:", values); // debug

        if (tempChart) {
            // Mise à jour du graphique existant
            tempChart.data.labels = labels;
            tempChart.data.datasets[0].data = values;
            tempChart.update();
        } else {
            // Création du graphique
            tempChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Température (°C)',
                        data: values,
                        borderColor: 'rgb(255, 99, 132)',
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        tension: 0.3,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { suggestedMin: 0, suggestedMax: 40 },
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
        console.error("Erreur fetch temp:", err);
    }
}

// ⚡ Attendre que la page soit chargée
document.addEventListener("DOMContentLoaded", () => {
    loadTempGraph();
    setInterval(loadTempGraph, 5000);
});
