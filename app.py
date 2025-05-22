from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

def conectar():
    os.makedirs("db", exist_ok=True)
    return sqlite3.connect('db/banco.db')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/produtos', methods=['GET'])
def listar_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    rows = cursor.fetchall()
    conn.close()
    produtos = [{
        'id': row[0],
        'codigo': row[1],
        'nome': row[2],
        'categoria': row[3],
        'quantidade': row[4],
        'preco': row[5],
        'estoque_minimo': row[6]
    } for row in rows]
    return jsonify(produtos)

@app.route('/api/produtos', methods=['POST'])
def adicionar_produto():
    data = request.json
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO produtos (codigo, nome, categoria, quantidade, preco, estoque_minimo)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data['codigo'],
        data['nome'],
        data['categoria'],
        data['quantidade'],
        data['preco'],
        data['estoque_minimo']
    ))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Produto adicionado com sucesso!'})

@app.route('/api/entradas', methods=['POST'])
def registrar_entrada():
    data = request.json
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO entradas (produto_id, quantidade, data, fornecedor, observacao)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data['produto_id'],
        data['quantidade'],
        data['data'],
        data['fornecedor'],
        data.get('observacao', '')
    ))
    cursor.execute("""
        UPDATE produtos SET quantidade = quantidade + ?
        WHERE id = ?
    """, (data['quantidade'], data['produto_id']))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Entrada registrada!'})

@app.route('/api/saidas', methods=['POST'])
def registrar_saida():
    data = request.json
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO saidas (produto_id, quantidade, data, destino, observacao)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data['produto_id'],
        data['quantidade'],
        data['data'],
        data['destino'],
        data.get('observacao', '')
    ))
    cursor.execute("""
        UPDATE produtos SET quantidade = quantidade - ?
        WHERE id = ?
    """, (data['quantidade'], data['produto_id']))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Saída registrada!'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (data['usuario'], data['senha']))
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({'mensagem': 'Login bem-sucedido!', 'usuario': user[2]})
    return jsonify({'erro': 'Usuário ou senha inválidos'}), 401

@app.route('/api/registro', methods=['POST'])
def registro():
    data = request.json
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nome, usuario, senha) VALUES (?, ?, ?)", (
            data['nome'], data['usuario'], data['senha']
        ))
        conn.commit()
        return jsonify({'mensagem': 'Usuário cadastrado!'})
    except sqlite3.IntegrityError:
        return jsonify({'erro': 'Usuário já existe'}), 400
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
