import os
import json
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHANNEL_ID = "@baixatudo"
CATALOG_FILE = "catalog.json"

def load_catalog():
    if not os.path.exists(CATALOG_FILE):
        return []
    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_catalog(catalog):
    with open(CATALOG_FILE, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    categoria = request.form.get("categoria", "Outro")
    if not file:
        return jsonify({"error": "Ficheiro em falta"}), 400

    filename = file.filename
    files = {"document": (filename, file.stream, file.mimetype)}
    data = {
        "chat_id": CHANNEL_ID,
        "caption": f"{categoria} | {filename}"
    }

    send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    resp = requests.post(send_url, data=data, files=files)

    if resp.status_code != 200:
        return jsonify({"error": "Erro ao enviar para Telegram"}), 500

    file_id = resp.json()["result"]["document"]["file_id"]

    # Guardar no catálogo
    catalog = load_catalog()
    catalog.append({
        "file_id": file_id,
        "file_name": filename,
        "categoria": categoria
    })
    save_catalog(catalog)

    return jsonify({"success": True, "file_name": filename})

@app.route("/catalog", methods=["GET"])
def get_catalog():
    return jsonify(load_catalog())