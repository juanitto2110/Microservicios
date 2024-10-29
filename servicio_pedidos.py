from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)

# Simulated database
pedidos = [
    {"id": 1, "usuario_id": 1, "producto": "Laptop", "cantidad": 1},
    {"id": 2, "usuario_id": 2, "producto": "Monitor", "cantidad": 2}
]

# Verify user by making a request to the user service
def verificar_usuario(usuario_id):
    try:
        response = requests.get(
            f'http://localhost:{os.getenv("USERS_SERVICE_PORT")}/api/usuarios/{usuario_id}'
        )
        return response.status_code == 200
    except requests.RequestException:
        return False

# GET all orders
@app.route('/api/pedidos', methods=['GET'])
def obtener_pedidos():
    return jsonify({
        "servicio": "pedidos",
        "data": pedidos,
        "status": "success"
    })

# GET orders by user ID
@app.route('/api/pedidos/<int:usuario_id>', methods=['GET'])
def obtener_pedidos_usuario(usuario_id):
    if not verificar_usuario(usuario_id):
        return jsonify({"error": "Usuario no válido", "status": "error"}), 404
    pedidos_usuario = [p for p in pedidos if p['usuario_id'] == usuario_id]
    return jsonify({
        "servicio": "pedidos",
        "data": pedidos_usuario,
        "status": "success"
    })

# Health check
@app.route('/api/pedidos/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "healthy", "service": "pedidos"})

if __name__ == '__main__':
    port = int(os.getenv('ORDERS_SERVICE_PORT', 5001))
    app.run(port=port, debug=True)