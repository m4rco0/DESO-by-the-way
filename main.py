from src.agents.lampiao_agent import AgenteLampiao
from src.database.sql_con import AnaDatabase

def main():
    JSON_PATH = 'src/testes/telemetria_gerada.json' 
    db = AnaDatabase(db_name="telemetria.db")
    db.importar_telemetria(JSON_PATH)
    resultados = db.buscar_leituras()
    

    agent = AgenteLampiao()
    agent.audicao_lote("Telemetria 01", resultados)
    db.close()


if __name__ == "__main__":
    main()