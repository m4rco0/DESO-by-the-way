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
    try:
        # Tenta pegar o ID da URL (?id=...), se não tiver, usa o padrão
        id_atual = request.args.get('id', "Teste de Carga 01")

        # Conversão do Markdown (como você já tinha)
        html_content = markdown.markdown(analise_geral)

        return render_template(
            "relatorio.html", 
            conteudo_analise=html_content,
            intervencao_id=id_atual  # <--- VOCÊ PRECISAVA ADICIONAR ISSO AQUI!
        )

    except Exception as e:
        traceback.print_exc()
        return f"<h1>Erro interno: {str(e)}</h1>", 500
    

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/api/chat-relatorio", methods=["POST"])
def chat_relatorio():
    data = request.get_json()
    pergunta = data.get("mensagem")
    intervencao_id = data.get("contexto_id") # O ID da intervenção


    print(f"Dados recebidos em /api/chat-relatorio: {data}")
    if not pergunta or not intervencao_id:
        return jsonify({"erro": "Dados incompletos"}), 400

    try:
        todos_dados = db.buscar_leituras() 
        
        # Filtro simples em Python (se seu DB não tiver filtro por ID ainda)
        dados_da_intervencao = [d for d in todos_dados if d['intervencao_id'] == intervencao_id]

        if not dados_da_intervencao:
            return jsonify({"resposta": "Não encontrei dados para essa intervenção."})

        # 2. O Agente analisa a pergunta com base nesses dados
        resposta = agent.responder_duvida(
            dados_brutos=dados_da_intervencao, 
            pergunta=pergunta
        )

        return jsonify({"resposta": resposta})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"erro": str(e)}), 500

print(app.url_map)

app.run('0.0.0.0', 8080)