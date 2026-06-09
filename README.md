# plataforma-monitoramento-devops
# 🚀 Plataforma de Monitoramento DevOps

Este projeto consiste em uma **Plataforma de Monitoramento de Serviços de Rede** em tempo real, desenvolvida como Trabalho Final para a disciplina de Redes de Computadores e Internet no IDP, sob a orientação da Profa. Lorena Borges.

A aplicação foi projetada para capturar, persistir e alertar sobre o estado de integridade de múltiplos serviços essenciais de infraestrutura (Web Server, Banco de Dados, DNS e SMTP), simulando cenários reais de operação e segurança.

## 🏗️ Arquitetura do Sistema

O ecossistema foi estruturado seguindo o modelo de microsserviços e orientado a eventos, mapeando os hosts monitorados, a camada de coleta, a ingestão dos dados e a visualização no painel:

```mermaid
graph TB
    subgraph INFRA [Infraestrutura Monitorada - Hosts Sintéticos]
        H1["🖥️ Host 01: WebServer-Prod-01<br>(Apache HTTP Server)<br>• Métricas: RPS, Latência<br>• CVE-2023-25690"]
        H2["🖥️ Host 02: DBServer-Prod-02<br>(PostgreSQL DB)<br>• Métricas: CPU, Conexões<br>• CVE-2024-10979"]
        H3["🖥️ Host 03: DNSServer-Core-01<br>(BIND9 DNS Server)<br>• Métricas: Queries/s, Erros<br>• CVE-2023-2828"]
    end

    subgraph CODESPACE [Ambiente GitHub Codespaces Sandbox]
        subgraph AGENT_LAYER [Camada de Coleta]
            AG["⚙️ traffic_simulator.py<br>(Agente de Telemetria)"]
        end

        subgraph BACKEND [Camada de Ingestão & Lógica]
            API["🚀 BACKEND API<br>(FastAPI / Uvicorn)<br>Porta 8000"]
        end

        subgraph DATA [Camada de Persistência]
            DB["🗄️ BANCO DE DADOS<br>(SQLite Async)<br>metrics.db"]
        end

        subgraph ALERTS [Ação Automatizada]
            NOTIF["📧 SISTEMA DE NOTIFICAÇÃO<br>(BackgroundTasks - SMTP/Log)"]
        end
    end

    subgraph CLIENT [Camada de Visualização - Usuário]
        FRONT["🌐 FRONTEND DASHBOARD<br>(Navegador Web / JS)<br>Porta 3000"]
    end

    %% Fluxos de Comunicação e Protocolos de Rede
    H1 -->|Coleta Local| AG
    H2 -->|Coleta Local| AG
    H3 -->|Coleta Local| AG

    AG -->|HTTP POST / JSON| API
    API -->|Gravação Assíncrona| DB
    API -->|Disparo de Alerta Event-Driven| NOTIF
    FRONT -->|HTTP GET / Polling Periódico| API

    %% Estilização de Design Profissional
    style INFRA fill:#f5f5f5,stroke:#9e9e9e,stroke-width:2px,stroke-dasharray: 5 5
    style CODESPACE fill:#e1f5fe,stroke:#0288d1,stroke-width:2px
    style CLIENT fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    style API fill:#e8f5e9,stroke:#388e3c,stroke-width:2px
    style DB fill:#eceff1,stroke:#455a64,stroke-width:2px
    style NOTIF fill:#ffebee,stroke:#d32f2f,stroke-width:2px
---

## 🛠️ Tecnologias Utilizadas

* **Front-end:** HTML5, Tailwind CSS (Design Responsivo) e JavaScript Assíncrono (Fetch API / Polling cíclico a cada 2000ms).
* **Back-end:** Python, FastAPI (Framework assíncrono de alta performance) e Uvicorn (Asynchronous Server Gateway Interface).
* **Banco de Dados:** SQLite (Armazenamento local binarizado para histórico de telemetria em `metrics.db`).
* **Ambiente de Desenvolvimento:** GitHub Codespaces (Cloud Base).

---

## 📊 Funcionalidades Implementadas

* **Visão Consolidada do Ecossistema:** Painel dinâmico que reflete o estado global do sistema (Verde, Amarelo, Vermelho).
* **Monitoramento de Métricas por Serviço:**
  * **Web Server:** Latência (ms), Requisições por Segundo (RPS), Códigos de Erro (4xx/5xx) e Conexões Ativas.
  * **Banco de Dados:** Consultas por Segundo (QPS), Uso de CPU/Memória, Crescimento de Armazenamento (GB/dia) e Queries Lentas.
  * **DNS & SMTP:** Resolução de nomes, taxa de entrega e tamanho da fila de e-mails em tempo real.
* **Mecanismo de Segurança e Alertas:** Detecção de picos anômalos de tráfego (DDoS), tentativas de força bruta (Brute-Force), alterações em arquivos de configuração e mapeamento de vulnerabilidades conhecidas (CVE).

---

## 📂 Estrutura do Repositório

```text
├── backend/
│   ├── app.py              # API de Ingestão de Métricas (FastAPI)
│   ├── requirements.txt    # Dependências de pacotes do ecossistema Python
│   └── simulator.py        # Motor de simulação de telemetria de rede
├── frontend/
│   ├── index.html          # Dashboard e Interface do Usuário
│   ├── script.js           # Lógica de consumo da API e renderização de gráficos
│   └── style.css           # Arquivo de estilos (otimizado via Tailwind CDN)
├── .gitignore              # Configuração de arquivos ignorados pelo Git
├── DOCUMENTACAO.md         # Relatório Técnico Completo (Arquitetura, Runbooks e Playbooks)
├── metrics.db              # Banco de dados SQLite persistido (Auto-generated)
└── README.md               # Apresentação do projeto (Este arquivo)