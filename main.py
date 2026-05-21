from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from groq import Groq
import os
from core.prompt_mestre import prompt_mestre

app = Flask(__name__)

# aqui é definida a chave de sessão (obrigatório o uso de uma API key para o Groq, que deve ser definida na variável de ambiente GROQ_API_KEY a API key pode ser obtida gratuitamente no site do Groq: https://groq.com/)
# API key deve ser configurada no terminal (powershell ou bash) antes de iniciar 

app.secret_key = "segredo_super_secreto"

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

#  ROTA DE LOGIN (metodo post)
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

#  validação simples (apenas para demonstração verifica se email e senha são iguais aos pre-definidos)
        if email == "fabricio@gmail.com" and senha == "12345678":
            session["logado"] = True
            return redirect(url_for("chat_page"))
        else:
            return "Login inválido"

    return render_template("index.html")


#rotas
@app.route("/chat")
def chat_page():
    if not session.get("logado"):
        return redirect(url_for("login"))
    return render_template("chat.html")

#sobre 
@app.route("/sobre")
def sobre():
    if not session.get("logado"):
        return redirect(url_for("login"))
    return render_template("sobre.html")

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
@app.route("/api/chat", methods=["POST"])
def api_chat():
    try:
        if not session.get("logado"):
         return jsonify({"reply": "Não autorizado"}), 403
        data = request.get_json()
        msg = data["message"]

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": prompt_mestre},
                {"role": "user", "content": msg}
            ]
        )

        reply = response.choices[0].message.content

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)