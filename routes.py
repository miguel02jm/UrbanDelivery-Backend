from flask import request, jsonify
from app import app
from functions import dijkstra, path_to_movement, encodedMap_to_graph
from variables import rows, cols, mapa_code, mqtt_messages
from client_mqtt import mqtt_client, topic

@app.route('/InteligenciaAmbiental/recibirMapaCode', methods=['GET'])
def get_mqtt_messages():
    global mqtt_messages
    return jsonify({"message": mqtt_messages.strip()})

@mqtt_client.on_message()
def handle_and_get_mqtt_message(client, userdata, message):
    global mqtt_messages
    mqtt_messages = message.payload.decode('utf-8')
    with app.app_context():
        response = get_mqtt_messages()
    return mqtt_messages

@app.route('/InteligenciaAmbiental/enviarSalidaLlegada', methods=['POST'])
def publish_message():
    global resultado
    resultado = encodedMap_to_graph(rows, cols, mapa_code)
    if request.method == 'POST':
        request_data = request.get_json()
        if resultado is None:
            return jsonify({'mensaje': 'Aún no se ha procesado el mapa'})
        data = request.get_json()
        ini = int(data['salida'])
        fin = int(data['llegada'])
        path = dijkstra(resultado, ini, fin)
        movement = path_to_movement(path, cols=cols, rows=rows)
        movements_str = ','.join(movement)
        publish_result = mqtt_client.publish(topic, movements_str)
        return jsonify({'code': publish_result[0]})

