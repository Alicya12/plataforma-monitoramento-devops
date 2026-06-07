# plataforma-monitoramento-devops
# 🚀 Plataforma de Monitoramento DevOps

Este projeto consiste em uma **Plataforma de Monitoramento de Serviços de Rede** em tempo real, desenvolvida como Trabalho Final para a disciplina de Redes de Computadores e Internet no IDP, sob a orientação da Profa. Lorena Borges.

A aplicação foi projetada para capturar, persistir e alertar sobre o estado de integridade de múltiplos serviços essenciais de infraestrutura (Web Server, Banco de Dados, DNS e SMTP), simulando cenários reais de operação e segurança.

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