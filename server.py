from flask import Flask, request, jsonify
from getmac import get_mac_address

app = Flask(__name__)

# Dictionnaire pour stocker les connexions par adresse MAC
connections = {}

@app.route('/')
def index():
    # Obtenir l'adresse MAC du client
    mac_address = get_mac_address(ip=request.remote_addr)
    if mac_address:
        # Incrémenter le compteur pour cette adresse MAC
        if mac_address not in connections:
            connections[mac_address] = 0
        connections[mac_address] += 1
        return jsonify(message=f"Nombre de connexions pour {mac_address}: {connections[mac_address]}")
    else:
        return jsonify(message="Impossible de récupérer l'adresse MAC."), 400

@app.route('/stats')
def stats():
    return jsonify(connections)

if __name__ == '__main__':
    app.run(debug=True)