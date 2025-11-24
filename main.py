from mangaba_agent import MangabaAgent
import json

agent = MangabaAgent()

NOME_ARQUIVO = 'src/testes/telemetria_gerada.json'
try:
    with open(NOME_ARQUIVO, 'r', encoding='utf-8') as arquivo:
        # A função json.load() lê o arquivo e converte o JSON em um dicionário Python
        dados_python = json.load(arquivo)
        
        print("✅ Dados JSON lidos e convertidos com sucesso para dicionário Python:")
        print(f"Tipo de dados lidos: {type(dados_python)}")
        print(f"dados JSON: {dados_python}")

        resposta = agent.chat(f"Analise esses dados e tente verificar os erros no monitoramento da agua: {dados_python}")
        print(f"Resposta do MangabaAgent: {resposta}")
except json.JSONDecodeError:
    print("❌ Erro: O arquivo não está em um formato JSON válido.")
except Exception as e:
    print(f"❌ Ocorreu um erro: {e}")

