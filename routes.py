from flask import request, jsonify
from app import app
from functions import dijkstra, path_to_movement, encodedMap_to_graph, delivery2movement
from variables import rows, cols, mapa_code, mapa_code, pos_inicial_robot, pos_robot
from client_mqtt import mqtt_client, topic

@app.route('/recibirMapaCode', methods=['GET'])
def get_mapa_code():
    global mapa_code
    return jsonify({"mapaCode": mapa_code.strip()})

@app.route("/recibirPosicionRobot", methods=['GET'])
def get_pos_robot():
    global pos_robot
    return jsonify({"posRobot": pos_robot})

@mqtt_client.on_message()
def handle_messages(client, userdata, message):
    global mapa_code
    global pos_robot

    response = None

    if message.topic == '/map':
        mapa_code = message.payload.decode('utf-8')
        with app.app_context():
            response = get_mapa_code()
    elif message.topic == '/posRobot':
        pos_robot = message.payload.decode('utf-8')
        with app.app_context():
            response = get_pos_robot()

    if response is not None:
        return response
    else:
        with app.app_context():
            return jsonify({'error': 'No response'})

@app.route('/enviarSalidaLlegada', methods=['POST'])
def publish_message():
    global resultado, pos_inicial_robot
    resultado = encodedMap_to_graph(rows, cols, mapa_code)
    if request.method == 'POST':
        if resultado is None:
            return jsonify({'mensaje': 'Aún no se ha procesado el mapa'})
        data = request.get_json()
        ini = int(data['salida'])
        fin = int(data['llegada'])
        movement = delivery2movement(ini, fin, pos_inicial_robot, resultado)
        pos_inicial_robot = fin
        movements_str = ','.join(movement)
        publish_result = mqtt_client.publish(topic, movements_str)
        return jsonify({'code': publish_result[0]})

