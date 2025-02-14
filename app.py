from flask import Flask, jsonify
from flask_cors import CORS
import websocket
import threading
import json
import time

app = Flask(__name__)
CORS(app)

latest_price = {"price": "0.00"}  # Variable para almacenar el precio recibido

def update_price(message):
    global latest_price
    try:
        data = json.loads(message)
        latest_price["price"] = data["p"]  # Extraer el precio actual de EUR/USDT
        print(f"✅ Nuevo precio recibido: {latest_price['price']}")  # Debug en logs
    except Exception as e:
        print(f"❌ Error procesando mensaje del WebSocket: {e}")

def binance_ws():
    """ Mantiene la conexión WebSocket con Binance activa en Railway """
    print("🔄 Conectando al WebSocket de Binance...")
    while True:
        try:
            ws = websocket.WebSocketApp(
                "wss://stream.binance.com:9443/ws/eurusdt@trade",
                on_message=lambda ws, message: update_price(message),
                on_error=lambda ws, error: print(f"⚠️ WebSocket Error: {error}"),
                on_close=lambda ws, close_status, close_msg: print("🔄 WebSocket cerrado, reconectando...")
            )
            ws.run_forever()
        except Exception as e:
            print(f"⚠️ Error en WebSocket: {e}. Reintentando en 5 segundos...")
            time.sleep(5)

@app.route('/price', methods=['GET'])
def get_price():
    """ API para obtener el último precio """
    return jsonify(latest_price)

@app.route("/", methods=["GET"])
def home():
    """ Página de prueba para saber si el servidor está activo """
    return "Binance WebSocket API is running", 200

if __name__ == '__main__':
    print("🚀 Iniciando Flask en Railway...")
    threading.Thread(target=binance_ws, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
