from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

@app.route('/', methods=['POST'])
def post_results():
    data = request.json
    if not all(k in data for k in ['roundNumber', 'winners', 'losers']):
        return jsonify({"error": "Dados incompletos"}), 400
    if not DISCORD_WEBHOOK_URL:
        return jsonify({"error": "Webhook do Discord não configurado no servidor."}), 500
    embed = {
        "title": f"🏁 Fim da Rodada {data['roundNumber']} 🏁",
        "color": 0x5865F2,
        "fields": [
            {"name": "🏆 Vencedores (Avançaram)", "value": "\n".join(f"- {w}" for w in data['winners']) if data['winners'] else "N/A", "inline": True},
            {"name": "❌ Eliminados", "value": "\n".join(f"- {l}" for l in data['losers']) if data['losers'] else "N/A", "inline": True}
        ],
        "footer": {"text": "ALFA APOSTAS - Torneio"}
    }
    payload = { "embeds": [embed] }
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        return jsonify({"success": "Resultado enviado ao Discord."}), 200
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar para o Discord: {e}")
        return jsonify({"error": "Falha ao contatar o Discord."}), 500
