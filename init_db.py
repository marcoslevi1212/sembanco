import sqlite3
import os

os.makedirs("db", exist_ok=True)

conn = sqlite3.connect('db/banco.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    usuario TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL,
    nome TEXT NOT NULL,
    categoria TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    preco REAL NOT NULL,
    estoque_minimo INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS entradas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    data TEXT NOT NULL,
    fornecedor TEXT NOT NULL,
    observacao TEXT,
    FOREIGN KEY (produto_id) REFERENCES produtos (id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS saidas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    data TEXT NOT NULL,
    destino TEXT NOT NULL,
    observacao TEXT,
    FOREIGN KEY (produto_id) REFERENCES produtos (id)
)
""")

conn.commit()
conn.close()
print("Banco de dados criado com sucesso!")
