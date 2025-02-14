from flask import Flask, jsonify
from flask_cors import CORS
import websocket
import threading
import json

app = Flask(__name__)
CORS(app)  # Permitir solicitudes desde MIT App Inventor

latest_price = {"price": "0.00"}  # Variable para almacenar el último precio recibido

# WebSocket de Binance
def binance_ws():
    global latest_price
    def on_message(ws, message):
        data = json.loads(message)
        latest_price["price"] = data["p"]  # Extraer el precio del JSON recibido
        print(f"Nuevo precio recibido: {latest_price['price']}")  # Debug en logs

    ws = websocket.WebSocketApp(
        "wss://stream.binance.com:9443/ws/eurusdt@trade",
        on_message=on_message
    )
    ws.run_forever()

# Ruta de la API para obtener el último precio
@app.route('/price', methods=['GET'])
def get_price():
    return jsonify(latest_price)

# Ruta raíz para comprobar si el servidor está activo
@app.route("/", methods=["GET"])
def home():
    return "Binance WebSocket API is running", 200

# Iniciar WebSocket en un hilo separado
if __name__ == '__main__':
    threading.Thread(target=binance_ws, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)

