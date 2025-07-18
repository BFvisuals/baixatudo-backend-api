from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = "@baixatudo"

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "Ficheiro em falta"}), 400

    file = request.files['file']
    categoria = request.form.get('categoria', '📁 Outro')

    caption = f"📂 Categoria: {categoria}"
    files = {'document': (file.filename, file.stream, file.content_type)}
    data = {'chat_id': CHANNEL_ID, 'caption': caption}

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
    response = requests.post(url, data=data, files=files)

    if response.status_code == 200:
        return jsonify({"status": "sucesso"}), 200
    else:
        return jsonify({"error": response.text}), 500