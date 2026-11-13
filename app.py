
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# Conectar ao banco de dados
def conectar_banco():
    conexao = sqlite3.connect("usuarios.db")
    conexao.row_factory = sqlite3.Row
    return conexao


# Criar tabela de usuários
def criar_tabela():
    conexao = conectar_banco()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT
        )
    """)

    conexao.commit()
    conexao.close()


# Página inicial - Listar usuários
@app.route("/")
def inicio():
    conexao = conectar_banco()

    usuarios = conexao.execute(
        "SELECT * FROM usuarios"
    ).fetchall()

    conexao.close()

    return render_template("index.html", usuarios=usuarios)


# Cadastrar usuário
@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    nome = request.form["nome"]
    email = request.form["email"]
    telefone = request.form["telefone"]

    conexao = conectar_banco()

    conexao.execute(
        "INSERT INTO usuarios (nome, email, telefone) VALUES (?, ?, ?)",
        (nome, email, telefone)
    )

    conexao.commit()
    conexao.close()

    return redirect("/")


# Editar usuário
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conexao = conectar_banco()

    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        telefone = request.form["telefone"]

        conexao.execute(
            "UPDATE usuarios SET nome=?, email=?, telefone=? WHERE id=?",
            (nome, email, telefone, id)
        )

        conexao.commit()
        conexao.close()

        return redirect("/")

    usuario = conexao.execute(
        "SELECT * FROM usuarios WHERE id=?",
        (id,)
    ).fetchone()

    conexao.close()

    return render_template("editar.html", usuario=usuario)


# Excluir usuário
@app.route("/excluir/<int:id>")
def excluir(id):
    conexao = conectar_banco()

    conexao.execute(
        "DELETE FROM usuarios WHERE id=?",
        (id,)
    )

    conexao.commit()
    conexao.close()

    return redirect("/")


# Executar aplicação
if __name__ == "__main__":
    criar_tabela()
    app.run(debug=True)
