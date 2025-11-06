from flask import Flask, request, render_template_string, redirect, url_for
import base64

app = Flask(__name__)

# --- Funções de criptografia e descriptografia ---

def cifra_vigenere_utf8(mensagem, chave=""):
    if not chave:
        chave = "NAVIO2025"
    resultado = []
    tam_chave = len(chave)

    for i, caractere in enumerate(mensagem):
        valor_msg = ord(caractere)
        valor_chave = ord(chave[i % tam_chave])
        novo_valor = (valor_msg + valor_chave) % 0x10FFFF
        resultado.append(chr(novo_valor))

    # converte para base64 para exibição segura
    texto_cifrado = ''.join(resultado)
    texto_b64 = base64.b64encode(texto_cifrado.encode('utf-8')).decode('utf-8')
    return texto_b64


def decifra_vigenere_utf8(mensagem_cifrada, chave=""):
    if not chave:
        chave = "NAVIO2025"

    # Tenta decodificar de Base64
    try:
        mensagem_cifrada = base64.b64decode(mensagem_cifrada.encode('utf-8')).decode('utf-8')
    except Exception:
        return "Erro: mensagem cifrada inválida (verifique se foi gerada por este sistema)."

    resultado = []
    tam_chave = len(chave)

    for i, caractere in enumerate(mensagem_cifrada):
        valor_msg = ord(caractere)
        valor_chave = ord(chave[i % tam_chave])
        novo_valor = (valor_msg - valor_chave) % 0x10FFFF
        resultado.append(chr(novo_valor))

    return ''.join(resultado)


# --- Função para limpar os campos ---
def reset():
    """Limpa os campos da interface (mensagem, chave e resultado)."""
    return redirect(url_for("index"))


# --- Interface Web ---
HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Cifra de Vigenère UTF-8</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f4f7fb; color: #333; }
        h1 { color: #0a3d62; }
        textarea, input[type=text] { width: 100%; padding: 8px; border-radius: 8px; border: 1px solid #ccc; }
        .buttons { margin-top: 10px; display: flex; gap: 10px; }
        input[type=submit] { flex: 1; padding: 10px 20px; border: none; border-radius: 8px; background: #0a3d62; color: white; cursor: pointer;}
        input[type=submit]:hover { background: #1e5a88; }
        .reset { background: #a33; }
        .reset:hover { background: #d55; }
        pre { background: white; padding: 15px; border-radius: 8px; overflow-x: auto; }
    </style>
</head>
<body>
    <h1>Cifra de Vigenère (UTF-8 + Base64)</h1>
    <form method="post">
        <label>Mensagem:</label><br>
        <textarea name="mensagem" rows="4">{{mensagem}}</textarea><br><br>
        <label>Chave:</label><br>
        <input type="text" name="chave" value="{{chave}}" placeholder="Deixe vazio para usar NAVIO2025"><br><br>
        <div class="buttons">
            <input type="submit" name="acao" value="Criptografar">
            <input type="submit" name="acao" value="Descriptografar">
            <input type="submit" name="acao" value="Resetar" class="reset">
        </div>
    </form>
    {% if resultado %}
        <hr>
        <h3>Resultado:</h3>
        <pre>{{resultado}}</pre>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    mensagem = chave = resultado = ""

    if request.method == "POST":
        acao = request.form["acao"]

        if acao == "Resetar":
            return reset()

        mensagem = request.form["mensagem"].strip()
        chave = request.form["chave"].strip()

        if acao == "Criptografar":
            resultado = cifra_vigenere_utf8(mensagem, chave)
        elif acao == "Descriptografar":
            resultado = decifra_vigenere_utf8(mensagem, chave)

    return render_template_string(HTML, mensagem=mensagem, chave=chave, resultado=resultado)


if __name__ == "__main__":
    app.run(debug=True)
