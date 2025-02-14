from flask import Flask, jsonify
from flask_cors import CORS
import websocket
import threading
import json
import time

app = Flask(__name__)
CORS(app)  # Permite solicitudes desde MIT App Inventor

latest_price = {"price": "0.00"}  # Almacena el último precio recibido

# Función para actualizar el precio desde el WebSocket
def update_price(message):
    global latest_price
    try:
        data = json.loads(message)
        latest_price["price"] = data["p"]  # Extraer el precio del JSON recibido
        print(f"Nuevo precio recibido: {latest_price['price']}")  # 🔍 Debug en logs
    except Exception as e:
        print(f"Error procesando mensaje del WebSocket: {e}")

# Función para conectarse al WebSocket de Binance con reconexión automática
def binance_ws():
    print("🔄 Iniciando conexión WebSocket con Binance...")  # 🔍 Debug
    while True:
        try:
            print("🌐 Intentando conectar al WebSocket de Binance...")
            ws = websocket.WebSocketApp(
                "wss://stream.binance.com:9443/ws/eurusdt@trade",
                on_message=lambda ws, message: update_price(message),
                on_error=lambda ws, error: print(f"❌ WebSocket Error: {error}"),
                on_close=lambda ws, close_status, close_msg: print("🔄 WebSocket cerrado, intentando reconectar...")
            )
            ws.run_forever()
        except Exception as e:
            print(f"⚠️ Error en WebSocket: {e}. Reintentando en 5 segundos...")
            time.sleep(5)

# Ruta de la API para obtener el último precio
@app.route('/price', methods=['GET'])
def get_price():
    print("📩 Se recibió solicitud en /price")  # Debug
    return jsonify(latest_price)

# Ruta raíz para comprobar si el servidor está activo
@app.route("/", methods=["GET"])
def home():
    return "Binance WebSocket API is running", 200

# Iniciar el WebSocket en un hilo separado para no bloquear el servidor Flask
if __name__ == '__main__':
    print("🚀 Iniciando Flask en Render...")
    threading.Thread(target=binance_ws, daemon=True).start()  # Hilo en segundo plano
    app.run(host='0.0.0.0', port=10000)
