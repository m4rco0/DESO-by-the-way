from mangaba_agent import MangabaAgent
from src.database.sql_con import AnaDatabase
import os
import json
JSON_PATH = 'src/testes/telemetria_gerada.json'

lampiao = MangabaAgent(
    api_key= os.getenv('GOOGLE_API_KEY'),
    agent_id='lampião',
    enable_mcp=True
)
db = AnaDatabase(db_name="telemetria.db")
db.importar_telemetria(JSON_PATH)

print("\n--- CONSULTA 1: Todas as leituras ---")
todas_leituras = db.buscar_leituras()
for l in todas_leituras:
    print(f"ID: {l['id']} | time: {l['horario']} vazao: {l['vazao']} volume: {l['volume']} codigo de transmissão: {l['codigoTransmissao']} ")

print("---  Mandando para o prompt do mangaba os dados")



resposta = lampiao.chat(f" Verifique os codigos de transmissão e  a difereça de vazao em relação ao volume deacordo com o calculo da DESO ( companhia de agua do Brasil) e faça uma pequeno relatorio de quando os dados estão corretos. Dados: {todas_leituras}")

print(resposta)