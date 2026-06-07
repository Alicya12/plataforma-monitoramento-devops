import random

def generate_network_metrics():
    """
    Gera métricas em tempo real simulando o comportamento de serviços de rede.
    Inclui variações normais e a possibilidade de injetar anomalias de segurança.
    """
    # Define se vamos simular um ataque DDoS neste ciclo (5% de chance)
    is_ddos_attack = random.random() < 0.05
    # Define se vamos simular um ataque de força bruta (5% de chance)
    is_brute_force = random.random() < 0.05

    return {
        "web_server": {
            "status": "DOWN" if random.random() < 0.02 else "UP", # 2% de chance de queda [cite: 20]
            "latency_ms": round(random.uniform(500, 1500), 2) if is_ddos_attack else round(random.uniform(15, 85), 2), # Pico se houver DDoS [cite: 22]
            "rps": random.randint(800, 1200) if is_ddos_attack else random.randint(10, 45), # RPS estoura no DDoS [cite: 21, 46]
            "errors_4xx": random.randint(0, 3), # [cite: 23]
            "errors_5xx": random.randint(5, 20) if is_ddos_attack else random.randint(0, 1) # [cite: 23]
        },
        "database": {
            "status": "UP" if random.random() > 0.01 else "DOWN", # [cite: 26]
            "qps": random.randint(50, 200), # [cite: 27]
            "cpu_usage_percent": round(random.uniform(80, 99), 1) if is_ddos_attack else round(random.uniform(10, 40), 1), # [cite: 28]
            "slow_queries": random.randint(5, 12) if is_ddos_attack else random.randint(0, 1) # [cite: 28]
        },
        "dns": {
            "status": "UP", # [cite: 33]
            "resolution_time_ms": round(random.uniform(5, 30), 2), # [cite: 30]
            "failed_resolutions": random.randint(0, 2) if random.random() > 0.9 else 0 # [cite: 31]
        },
        "smtp": {
            "status": "UP",
            "queue_length": random.randint(20, 50) if random.random() > 0.95 else random.randint(0, 3), # Backlog ocasional [cite: 36]
            "delivery_rate_percent": round(random.uniform(98.0, 100.0), 1) # [cite: 35]
        },
        "security_alerts": {
            "ddos_detected": is_ddos_attack, # [cite: 46]
            "brute_force_attempts": random.randint(15, 40) if is_brute_force else random.randint(0, 2), # [cite: 47]
            "config_file_changed": random.random() < 0.02 # 2% de chance de alteração de arquivo [cite: 48]
        }
    }