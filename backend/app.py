import random
import time
import sqlite3
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Plataforma de Monitoramento DevOps - API Profissional",
    description="Backend de Ingestão, Armazenamento de Métricas e Alertas"
)

# Liberar acesso do Codespaces / Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONFIGURAÇÃO DO BANCO DE DADOS (SQLite) ---
DB_NAME = "metrics.db"

def init_db():
    """Cria a tabela de histórico de métricas se ela não existir."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS telemetry_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            system_level TEXT,
            payload TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Inicializa o banco de dados assim que o app liga
init_db()


# --- SISTEMA DE NOTIFICAÇÃO DE ALERTA (E-mail) ---
# Variável global para rastrear o último estado e evitar o envio de e-mails duplicados a cada 2 segundos
LAST_SYSTEM_LEVEL = "Verde"

def send_alert_email(level, message, action):
    """Simula o disparo de um e-mail estruturado via protocolo SMTP."""
    print("\n" + "="*60)
    print(f"📧 [SMTP - ALERTA DISPARADO] Enviando e-mail para: equipe-devops@empresa.com")
    print(f"Assunto: [ALERTA {level.upper()}] Alteração de Estado no Sistema de Monitoramento")
    print("-"*60)
    print(f"Detalhes do Incidente:")
    print(f"  - Nível de Gravidade: {level}")
    print(f"  - Mensagem: {message}")
    print(f"  - Ação Automatizada Executada: {action}")
    print(f"  - Timestamp: {int(time.time())}")
    print("="*60 + "\n")
    
    # NOTA ACADÉMICA: Para conectar a um servidor real de e-mails, 
    # bastaria desindentar e configurar o bloco padrão do smtplib do Python:
    # import smtplib
    # from email.mime.text import MIMEText
    # msg = MIMEText(message)
    # msg['Subject'] = f"Alerta {level}"
    # ... server = smtplib.SMTP('smtp.mailtrap.io', 2525) ...


# --- ROTAS DA API ---

@app.get("/")
def read_root():
    return {"status": "online", "message": "API com Banco de Dados e Sistema de E-mail Ativos!"}

@app.get("/api/metrics")
def get_metrics():
    global LAST_SYSTEM_LEVEL

    # 1. Simulação Dinâmica do Estado Global do Sistema
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

    # LOGICA DE DISPARO DE E-MAIL: Só envia se o estado mudar para pior (Amarelo ou Vermelho)
    if system_level != LAST_SYSTEM_LEVEL:
        if system_level in ["Amarelo", "Vermelho"]:
            send_alert_email(system_level, system_message, system_action)
        LAST_SYSTEM_LEVEL = system_level

    # 2. Métricas do Servidor Web + Monitoramento de Vulnerabilidade Conhecida (CVE)
    web_server_metrics = {
        "status": "UP",
        "latency_ms": random.randint(12, 68),
        "rps": random.randint(120, 480),
        "errors_4xx": random.randint(0, 4),
        "errors_5xx": random.randint(0, 1),
        "active_connections": random.randint(45, 180),
        "cve_status": "Secure (Apache/2.4.58 - No known CVEs)"
    }
    
    # 3. Métricas do Banco de Dados + Monitoramento de Vulnerabilidade Conhecida (CVE)
    database_metrics = {
        "status": "UP",
        "qps": random.randint(180, 550),
        "cpu_usage_percent": random.randint(15, 60),
        "memory_usage_percent": random.randint(35, 72),
        "slow_queries": random.randint(0, 2),
        "db_size_gb": 124.50 + round(random.uniform(0.01, 0.05), 2),
        "growth_gb_day": round(random.uniform(0.5, 1.2), 2),
        "cve_status": "Compliant (PostgreSQL 16.1 - Patched CVE-2023-5860)"
    }

    # 4. Métricas de DNS
    dns_metrics = {
        "status": "UP",
        "resolution_time_ms": random.randint(2, 15),
        "failed_resolutions": random.randint(0, 1),
        "queries_per_second": random.randint(950, 1200),
        "cve_status": "Secure (BIND 9.18 - No active vulnerabilities)"
    }

    # 5. Métricas de SMTP (E-mail)
    smtp_metrics = {
        "status": "UP",
        "delivery_rate_percent": round(random.uniform(98.5, 100.0), 1),
        "errors_count": random.randint(0, 3),
        "queue_length": random.randint(0, 12),
        "emails_per_minute": random.randint(20, 60),
        "cve_status": "Secure (Postfix 3.8 - Confirmed)"
    }

    # 6. Alertas de Segurança Avançados
    security_alerts_metrics = {
        "ddos_detected": True if system_level == "Vermelho" else False,
        "brute_force_attempts": random.randint(0, 8),
        "config_file_changed": random.choice([False, False, False, True, False])
    }
    
    # Montagem do payload completo esperado pelo frontend
    response_payload = {
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

    # --- PERSISTÊNCIA EM BANCO DE DADOS REAL ---
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        # Salva o timestamp, o nível e converte todo o JSON em texto para armazenar o histórico completo
        cursor.execute(
            "INSERT INTO telemetry_history (timestamp, system_level, payload) VALUES (?, ?, ?)",
            (int(time.time()), system_level, json.dumps(response_payload))
        )
        conn.commit()
        conn.close()
    except Exception as db_error:
        print(f"❌ Erro ao salvar no SQLite: {db_error}")

    return response_payload