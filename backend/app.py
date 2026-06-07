from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.simulator import generate_network_metrics

app = FastAPI(title="Plataforma de Monitoramento DevOps")

# Configuração do CORS para permitir que o seu futuro Frontend acesse a API
# Isso impede bloqueios de segurança do navegador dentro do Codespaces
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def evaluate_alert_level(metrics):
    """
    Avalia o estado das métricas em tempo real e define o nível de criticidade.
    Aplica as regras exigidas no roteiro de Redes de Computadores.
    """
    web = metrics["web_server"]
    db = metrics["database"]
    sec = metrics["security_alerts"]
    
    # Nível 3 - Vermelho (Crítico): serviço degradado ou indisponível
    if web["status"] == "DOWN" or db["status"] == "DOWN" or sec["ddos_detected"]:
        return {
            "level": "CRITICAL",
            "color": "red",
            "message": "ALERTA MÁXIMO: Serviço indisponível ou anomalia crítica (DDoS) detectada!",
            "action": "Notificação imediata enviada por e-mail para o administrador."
        }
    
    # Nível 2 - Amarelo (Atenção): indica degradação que exige observação
    elif web["latency_ms"] > 70 or db["cpu_usage_percent"] > 75 or sec["brute_force_attempts"] > 5 or sec["config_file_changed"]:
        return {
            "level": "WARNING",
            "color": "yellow",
            "message": "ATENÇÃO: Parâmetros operacionais degradados ou alteração suspeita detectada.",
            "action": "Notificação de alerta encaminhada por e-mail."
        }
    
    # Nível 1 - Verde (OK): estado normal
    return {
        "level": "OK",
        "color": "green",
        "message": "Todos os serviços operando dentro da normalidade.",
        "action": "Nenhuma ação necessária."
    }

@app.get("/api/metrics")
def get_metrics():
    """
    Rota principal da API que consolida as métricas simuladas e o status de alerta.
    """
    current_metrics = generate_network_metrics()
    alert_status = evaluate_alert_level(current_metrics)
    
    return {
        "system_status": alert_status,
        "services": current_metrics
    }