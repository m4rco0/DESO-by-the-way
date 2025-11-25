# DESO-by-the-way

Projeto de exemplo para ingestão e análise de telemetria de vazão/volume, com um agente (agente "Lampião") que consome os dados e gera um relatório.

## Estrutura do repositório

- [main.py](main.py) — script de execução principal.
- [requirements.txt](requirements.txt) — dependências (ex.: `mangaba`).
- [src/agents/lampiao_agent.py](src/agents/lampiao_agent.py) — implementação do agente: [`src.agents.lampiao_agent.AgenteLampiao`](src/agents/lampiao_agent.py).
- [src/database/sql_con.py](src/database/sql_con.py) — camada simples de banco: [`src.database.sql_con.AnaDatabase`](src/database/sql_con.py) (métodos importantes: [`src.database.sql_con.AnaDatabase.importar_telemetria`](src/database/sql_con.py), [`src.database.sql_con.AnaDatabase.buscar_leituras`](src/database/sql_con.py)).
- [src/testes/telemetria_gerada.json](src/testes/telemetria_gerada.json) — exemplo de dados de entrada.

## Requisitos

- Python 3.8+
- Dependências no arquivo [requirements.txt](requirements.txt)

## Instalação rápida

1. Criar e ativar um ambiente virtual (opcional, recomendado):
```bash
# Linux / macOS
python -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

