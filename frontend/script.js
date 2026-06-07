// Configurações de renderização de gráficos lineares com Chart.js
const ctxWeb = document.getElementById('chartWeb').getContext('2d');
const ctxDb = document.getElementById('chartDb').getContext('2d');

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } },
    scales: {
        x: { display: false },
        y: { grid: { color: '#374151' }, ticks: { color: '#9CA3AF', fontSize: 10 } }
    }
};

const webChart = new Chart(ctxWeb, {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Latência Web', data: [], borderColor: '#3B82F6', tension: 0.3, fill: false }] },
    options: chartOptions
});

const dbChart = new Chart(ctxDb, {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Uso de CPU', data: [], borderColor: '#F97316', tension: 0.3, fill: false }] },
    options: chartOptions
});

function updateCharts(webLatency, dbCpu) {
    const timeLabel = new Date().toLocaleTimeString();

    if (webChart.data.labels.length > 10) { webChart.data.labels.shift(); webChart.data.datasets[0].data.shift(); }
    webChart.data.labels.push(timeLabel);
    webChart.data.datasets[0].data.push(webLatency);
    webChart.update();

    if (dbChart.data.labels.length > 10) { dbChart.data.labels.shift(); dbChart.data.datasets[0].data.shift(); }
    dbChart.data.labels.push(timeLabel);
    dbChart.data.datasets[0].data.push(dbCpu);
    dbChart.update();
}

async function fetchMetrics() {
    const backendInput = document.getElementById('backendUrl').value.trim();
    if (!backendInput) return;

    const baseUrl = backendInput.replace(/\/+$/, "");

    try {
        const response = await fetch(`${baseUrl}/api/metrics`);
        if (!response.ok) throw new Error("Erro de conexão com o endpoint");
        const data = await response.json();

        // 1. Visão Consolidada (Alerta Global e Tomada de Ações)
        const status = data.system_status;
        const banner = document.getElementById('globalAlertBanner');
        const badge = document.getElementById('alertBadge');
        
        document.getElementById('alertTitle').innerText = status.level;
        document.getElementById('alertMessage').innerText = status.message;
        document.getElementById('alertAction').innerText = `Ação executada: ${status.action}`;

        if (status.color === 'red') {
            banner.className = "p-4 rounded-lg bg-red-950/80 border border-red-700 text-red-200 flex flex-col md:flex-row justify-between items-start md:items-center gap-2 transition-all duration-300";
            badge.className = "px-2.5 py-1 rounded text-xs font-bold uppercase bg-red-600 text-white animate-pulse";
        } else if (status.color === 'yellow') {
            banner.className = "p-4 rounded-lg bg-yellow-950/80 border border-yellow-600 text-yellow-200 flex flex-col md:flex-row justify-between items-start md:items-center gap-2 transition-all duration-300";
            badge.className = "px-2.5 py-1 rounded text-xs font-bold uppercase bg-yellow-500 text-black";
        } else {
            banner.className = "p-4 rounded-lg bg-green-950/80 border border-green-700 text-green-200 flex flex-col md:flex-row justify-between items-start md:items-center gap-2 transition-all duration-300";
            badge.className = "px-2.5 py-1 rounded text-xs font-bold uppercase bg-green-600 text-white";
        }

        // 2. Dashboards de Métricas Individuais
        const services = data.services;

        // Web Server
        document.getElementById('web-status').innerText = services.web_server.status;
        document.getElementById('web-status').className = `px-2 py-0.5 rounded text-xs font-bold ${services.web_server.status === 'UP' ? 'bg-green-900 text-green-300' : 'bg-red-900 text-red-300'}`;
        document.getElementById('web-latency').innerText = `${services.web_server.latency_ms} ms`;
        document.getElementById('web-rps').innerText = `${services.web_server.rps} req/s`;
        document.getElementById('web-errors').innerText = `${services.web_server.errors_4xx} / ${services.web_server.errors_5xx}`;
        document.getElementById('web-connections').innerText = services.web_server.active_connections;

        // Banco de Dados
        document.getElementById('db-status').innerText = services.database.status;
        document.getElementById('db-status').className = `px-2 py-0.5 rounded text-xs font-bold ${services.database.status === 'UP' ? 'bg-green-900 text-green-300' : 'bg-red-900 text-red-300'}`;
        document.getElementById('db-qps').innerText = `${services.database.qps} qps`;
        document.getElementById('db-resources').innerText = `${services.database.cpu_usage_percent}% / ${services.database.memory_usage_percent}%`;
        document.getElementById('db-slow').innerText = services.database.slow_queries;
        document.getElementById('db-growth').innerText = `${services.database.db_size_gb.toFixed(2)} GB (+${services.database.growth_gb_day} GB/dia)`;

        // DNS
        document.getElementById('dns-status').innerText = services.dns.status;
        document.getElementById('dns-status').className = `px-2 py-0.5 rounded text-xs font-bold ${services.dns.status === 'UP' ? 'bg-green-900 text-green-300' : 'bg-red-900 text-red-300'}`;
        document.getElementById('dns-time').innerText = `${services.dns.resolution_time_ms} ms`;
        document.getElementById('dns-failed').innerText = services.dns.failed_resolutions;
        document.getElementById('dns-qps').innerText = `${services.dns.queries_per_second} qps`;

        // SMTP
        document.getElementById('smtp-status').innerText = services.smtp.status;
        document.getElementById('smtp-status').className = `px-2 py-0.5 rounded text-xs font-bold ${services.smtp.status === 'UP' ? 'bg-green-900 text-green-300' : 'bg-red-900 text-red-300'}`;
        document.getElementById('smtp-delivery').innerText = `${services.smtp.delivery_rate_percent}% / ${services.smtp.errors_count}`;
        document.getElementById('smtp-queue').innerText = services.smtp.queue_length;
        document.getElementById('smtp-volume').innerText = `${services.smtp.emails_per_minute} e-mails/min`;

        // Monitoramento de Segurança Avançado
        const sec = services.security_alerts;
        const ddosElement = document.getElementById('sec-ddos');
        if (sec.ddos_detected) {
            ddosElement.innerText = "🚨 ATAQUE DETECTADO";
            ddosElement.className = "px-2 py-0.5 rounded text-xs font-bold bg-red-600 text-white animate-bounce";
        } else {
            ddosElement.innerText = "NORMAL";
            ddosElement.className = "px-2 py-0.5 rounded text-xs font-bold bg-green-900 text-green-300";
        }

        document.getElementById('sec-brute').innerText = `${sec.brute_force_attempts} falhas recentes`;
        document.getElementById('sec-brute').className = `text-sm font-mono font-bold ${sec.brute_force_attempts > 5 ? 'text-yellow-400' : 'text-gray-300'}`;

        const configElement = document.getElementById('sec-config');
        if (sec.config_file_changed) {
            configElement.innerText = "⚠️ MODIFICADO RECENTEMENTE";
            configElement.className = "px-2 py-0.5 rounded text-xs font-bold bg-yellow-600 text-black";
        } else {
            configElement.innerText = "ÍNTEGROS";
            configElement.className = "px-2 py-0.5 rounded text-xs font-bold bg-green-900 text-green-300";
        }

        // Atualização contínua dos gráficos lineares
        updateCharts(services.web_server.latency_ms, services.database.cpu_usage_percent);

    } catch (error) {
        console.error("Falha ao sincronizar telemetria:", error);
    }
}

// Ingestão cíclica a cada 2000ms (2 segundos)
setInterval(fetchMetrics, 2000);