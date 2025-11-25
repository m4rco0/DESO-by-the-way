import sqlite3
import json
import os

class AnaDatabase:
    """
    Gerencia a conexão e operações do banco de dados para a API ANA.
    """
    def __init__(self, db_name = "tutorial.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

        self._connect()
        self._criarTabelas()

        
    def _connect(self):
        print("- Conectando ao banco de dados")
        self.conn =sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def _criarTabelas(self):
        print("- Criando tabelas")
        # Tabela de Leituras
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS leituras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            intervencao_id TEXT NOT NULL,
            horario TEXT NOT NULL,
            vazao REAL,
            duracao INTEGER,
            volume REAL,
            codigoTransmissao INTEGER
        );""")

        # Tabela de Usuários (Corrigi 'usename' para 'username')
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        );""")
        
        self.conn.commit()
        print("\t[+] Tabelas estruturadas com sucesso!")

    def _inserir_leitura_unica(self, intervencao_id, leitura):
        """
        Verifica duplicidade e insere uma leitura.
        Retorna True se inseriu, False se pulou.
        """
        horario = leitura.get('horario')
        
        self.cursor.execute(
            "SELECT 1 FROM leituras WHERE intervencao_id = ? AND horario = ? LIMIT 1",
            (intervencao_id, horario)
        )
        if self.cursor.fetchone():
            print(f"\t[!] Duplicata detectada (ID: {intervencao_id}, Hora: {horario}). Pulando.")
            return False

        # Insere dados
        self.cursor.execute(
            """
            INSERT INTO leituras (intervencao_id, horario, vazao, duracao, volume, codigoTransmissao)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                intervencao_id, 
                horario, 
                leitura.get('vazao'), 
                leitura.get('duracao'), 
                leitura.get('volume'), 
                leitura.get('codigoTransmissao')
            )
        )
        return True
    
    def adicionar_usuario(self, username, senha):
        """Método utilitário para registrar usuários."""
        try:
            self.cursor.execute(
                "INSERT INTO usuarios (username, senha) VALUES (?, ?)", 
                (username, senha)
            )
            self.conn.commit()
            print(f"[+] Usuário {username} cadastrado.")
        except sqlite3.IntegrityError:
            print(f"[!] Usuário {username} já existe.")

    def importar_telemetria(self, json_path):

        print(f"[+] Iniciando arquivo JSON: {json_path}")
        if not os.path.exists(json_path):
            print(f"[!] Erro: path não existe: {json_path}")
            return 
        
        try:
            with open(json_path, 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
        except json.JSONDecodeError as e:
            print(f"[!] Error no econde do JSON: {e}")
            return

        inserted_count = 0

        def _processar_item(item):
            nonlocal inserted_count
            intervencao_id = item.get('intervencao_id')
            leituras = item.get('leituras', [])

            if not intervencao_id:
                print("\t[!] Aviso: 'intervencao_id' vazio ou não encontrado para um item. Pulando.")
                return

            if not leituras:
                print(f"\t[!] Nenhuma leitura encontrada no JSON para intervencao_id '{intervencao_id}'.")
                return

            for leitura in leituras:
                if self._inserir_leitura_unica(intervencao_id, leitura):
                    inserted_count += 1

        # aceita um array de objetos ou um único objeto
        if isinstance(dados, list):
            for item in dados:
                if isinstance(item, dict):
                    _processar_item(item)
                else:
                    print("\t[!] Item do array não é um objeto. Pulando.")
        elif isinstance(dados, dict):
            _processar_item(dados)
        else:
            print("\t[!] Formato de JSON não esperado. Deve ser um objeto ou um array de objetos.")
            return

        self.conn.commit()
        print(f"[+] Processo finalizado. {inserted_count} novas leituras inseridas.")

    def buscar_leituras(self, intervencao_id=None):
        """
        Busca leituras no banco. 
        Se passar um ID (str) filtra por ele.
        Se passar uma lista/tupla, filtra por vários usando IN.
        Se não, traz tudo.
        Retorna uma lista de dicionários.
        """
        if isinstance(intervencao_id, (list, tuple)) and intervencao_id:
            placeholders = ",".join("?" for _ in intervencao_id)
            query = f"SELECT * FROM leituras WHERE intervencao_id IN ({placeholders})"
            params = tuple(intervencao_id)
        elif intervencao_id:
            query = "SELECT * FROM leituras WHERE intervencao_id = ?"
            params = (intervencao_id,)
        else:
            query = "SELECT * FROM leituras"
            params = ()

        self.cursor.execute(query, params)
        linhas = self.cursor.fetchall()

        # Truque para converter a resposta (tupla) em Dicionário
        # Pega os nomes das colunas (id, intervencao_id, vazao...)
        colunas = [desc[0] for desc in self.cursor.description]
        
        resultados = []
        for linha in linhas:
            # Cria um dicionário juntando Nome da Coluna + Valor
            resultados.append(dict(zip(colunas, linha)))
            
        return resultados
    
    def close(self):
        if self.conn:
            self.conn.close()
            print("[+] Conexão foi fechada.")
