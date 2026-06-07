import random
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Plataforma de Monitoramento DevOps - API",
    description="Backend de Ingestão de Métricas"
)

# Liberar acesso do Codespaces
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "online", "message": "API Rodando!"}

@app.get("/api/metrics")
def get_metrics():
    # 1. Simulação do Estado Global do Sistema
    roll = random.random()
    if roll > 0.92:
        system_level = "Vermelho"
        system_message = "Alerta Crítico: Altas falhas consecutivas de segurança."
        system_action = "Bloqueio de IP ativado no Firewall"
        system_color = "red"
    elif roll > 0.80:
        system_level = "Amarelo"
        system_message = "Atenção: Sobrecarga leve detectada no banco de dados."
        system_action = "Escalonamento automático acionado"
        system_color = "yellow"
    else:
        system_level = "Verde"
        system_message = "Todos os sistemas operando normalmente."
        system_action = "Nenhuma (Monitoramento automatizado)"
        system_color = "green"

    # 2. Métricas do Servidor Web
    web_server_metrics = {
        "status": "UP",
        "latency_ms": random.randint(12, 68),
        "rps": random.randint(120, 480),
        "errors_4xx": random.randint(0, 4),
        "errors_5xx": random.randint(0, 1),
        "active_connections": random.randint(45, 180)
    }
    
    # 3. Métricas do Banco de Dados
    database_metrics = {
        "status": "UP",
        "qps": random.randint(180, 550),
        "cpu_usage_percent": random.randint(15, 60),
        "memory_usage_percent": random.randint(35, 72),
        "slow_queries": random.randint(0, 2),
        "db_size_gb": 124.50 + round(random.uniform(0.01, 0.05), 2),
        "growth_gb_day": round(random.uniform(0.5, 1.2), 2)
    }

    # 4. Métricas de DNS
    dns_metrics = {
        "status": "UP",
        "resolution_time_ms": random.randint(2, 15),
        "failed_resolutions": random.randint(0, 1),
        "queries_per_second": random.randint(950, 1200)
    }

    # 5. Métricas de SMTP (E-mail)
    smtp_metrics = {
        "status": "UP",
        "delivery_rate_percent": round(random.uniform(98.5, 100.0), 1),
        "errors_count": random.randint(0, 3),
        "queue_length": random.randint(0, 12),
        "emails_per_minute": random.randint(20, 60)
    }

    # 6. Alertas de Segurança
    security_alerts_metrics = {
        "ddos_detected": True if system_level == "Vermelho" else False,
        "brute_force_attempts": random.randint(0, 8),
        "config_file_changed": random.choice([False, False, False, True, False])
    }
    
    # Retorno estruturado exatamente como o script.js espera
    return {
        "system_status": {
            "level": system_level,
            "message": system_message,
            "action": system_action,
            "color": system_color
        },
        "services": {
            "web_server": web_server_metrics,
            "database": database_metrics,
            "dns": dns_metrics,
            "smtp": smtp_metrics,
            "security_alerts": security_alerts_metrics
        }
    }