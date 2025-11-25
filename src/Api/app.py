from flask import Flask, request, jsonify, render_template # <--- Adicione render_template
import markdown # <--- Adicione markdown
from src.database.sql_con import AnaDatabase
from src.agents.lampiao_agent import AgenteLampiao
import os
import traceback

app = Flask(__name__)

# ... (Instâncias do db e agent continuam iguais) ...
db = AnaDatabase()
agent = AgenteLampiao()
db.importar_telemetria("src/testes/telemetria_gerada.json")
res = db.buscar_leituras()
analise_geral = agent.audicao_lote(intervencao_id="Teste de Carga 01",dados_brutos=res)

@app.route("/relatorio-web", methods=["GET"])
def relatorio_web():
    """
    Rota para visualizar a análise no navegador.
    Uso: /relatorio-web?id=Teste de Carga 01
    """
    
    try:


        # 4. Converte Markdown para HTML
        html_content = markdown.markdown(analise_geral)

        # 5. Renderiza o template HTML
        return render_template(
            "relatorio.html", 
            conteudo_analise=html_content
        )

    except Exception as e:
        traceback.print_exc()
        return f"<h1>Erro interno: {str(e)}</h1>", 500