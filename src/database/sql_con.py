import sqlite3

# 1. Conecta/Cria o banco de dados
con = sqlite3.connect("tutorial.db")

# 2. Cria o cursor
cur = con.cursor()

cur.execute("""
INSERT INTO 
            """)

con.commit() 

# 5. Fecha a conexão
con.close() 
