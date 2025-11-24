import sqlite3
import json
# 1. Conecta/Cria o banco de dados
con = sqlite3.connect("tutorial.db")

# 2. Cria o cursor
cur = con.cursor()

dados = json.load("../testes/telemetria_gerada.json")
print(dados)
cur.execute("""
CREATE TABLE leituras (
    id INTEGER PRIMARY KEY,
    intervencao_id INTEGER NOT NULL,
    horario TEXT NOT NULL,
    vazao REAL,
    duracao INTEGER,
    volume REAL,
    codigoTransmissao INTEGER
);

CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY,
    usename TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL
);

INSERT INTO leituras (intervencao_id, horario, vazao, duracao, volume, codigoTransmissao) 
VALUES (10, '2025-11-24T18:52:21.013872-03:00', 3.87, 300, 1019.35, 100);

-- Leitura 2
INSERT INTO leituras (intervencao_id, horario, vazao, duracao, volume, codigoTransmissao)  VALUES (10, '2025-11-24T18:57:21.013872-03:00', 1.01, 300, 1024.4, 100);

-- Leitura 3
INSERT INTO leituras (intervencao_id, horario, vazao, duracao, volume, codigoTransmissao)  VALUES (10, '2025-11-24T19:02:21.013872-03:00', 3.43, 300, 1041.55, 100);

-- Leitura 4
INSERT INTO leituras (intervencao_id, horario, vazao, duracao, volume, codigoTransmissao) VALUES (10, '2025-11-24T19:07:21.013872-03:00', 2.92, 300, 1056.15, 100);

-- Leitura 5
INSERT INTO leituras (intervencao_id, horario, vazao, duracao, volume, codigoTransmissao) 
VALUES (10, '2025-11-24T19:12:21.013872-03:00', 3.8, 300, 1075.15, 100);
            """)

con.commit() 

# 5. Fecha a conexão
con.close() 
