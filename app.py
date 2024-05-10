# from flask import Flask, request, jsonify
# from flask_mqtt import Mqtt
# import networkx as nx

# app = Flask(__name__)
# app.config['MQTT_BROKER_URL'] = '10.82.146.13'
# app.config['MQTT_BROKER_PORT'] = 1883
# # app.config['MQTT_USERNAME'] = 'TP-LINK_7794'
# # app.config['MQTT_PASSWORD'] = '00280549'
# app.config['MQTT_REFRESH_TIME'] = 1.0

# mqtt = Mqtt(app)

# datos_recibidos = []
# mensaje_recibido = False  # Variable de estado para controlar si se ha recibido al menos un mensaje
# resultado = None
# rows = 7
# cols = 5
# movement = []
# initial_pos = 0

# @mqtt.on_connect()
# def handle_connect(client, userdata, flags, rc):
#     print("Conectado al broker MQTT")
#     mqtt.subscribe('$SYS/broker/version')

# @mqtt.on_message()
# def handle_message(client, userdata, message):
#     global datos_recibidos, mensaje_recibido, resultado
#     print("Mensaje recibido en el topic: ", message.topic)
#     print("Contenido del mensaje: ", message.payload.decode())
#     # Almacena los datos recibidos en la variable global
#     datos_recibidos.append(message.payload.decode())
#     mensaje_recibido = True  # Marca que se ha recibido al menos un mensaje
#     # Una vez recibido el mensaje, ejecutar la función y desuscribirse del topic
#     if mensaje_recibido:
#         mapa_code = datos_recibidos[0]  # Suponiendo que solo hay un mensaje recibido
#         # Llamar a la función encodedMap_to_graph
#         resultado = encodedMap_to_graph(rows, cols, mapa_code)
#         # Mostrar el resultado por pantalla
#         print(resultado)
#         # Desuscribirse del topic "map" una vez procesado el primer mensaje
#         mqtt.unsubscribe("map")

# @app.route('/InteligenciaAmbiental/enviarSalidaLlegada', methods=['POST'])
# def recibir_post():
#     global resultado
#     if request.method == 'POST':
#         # Recoger los datos del formulario enviado
#         data = request.form
#         ini = data.get('salida')  # Obtener el valor del primer String desde el formulario
#         fin = data.get('llegada')  # Obtener el valor del segundo String desde el formulario
#         # Ejecutar el algoritmo de Dijkstra con los parámetros recibidos
#         if resultado is not None:  # Verificar si el resultado de encodedMap_to_graph está disponible
#             path=dijkstra(resultado, ini, fin)
#             movement = path_to_movement(path,cols=cols,rows=rows)
#             res = delivery2movement(ini, fin, initial_pos, resultado)
#             initial_pos = fin
#             mqtt.publish('A3-467/GrupoX/movimientos', ', '.join(movement))
#             mqtt.publish('A3-467/GrupoX/ruta', ', '.join(path))
#             return jsonify({'mensaje': 'Datos procesados correctamente'})  # Devuelve una respuesta indicando que los datos se han procesado correctamente
#         else:
#             return jsonify({'mensaje': 'Aún no se ha procesado el mapa'})

# @app.route("/InteligenciaAmbiental/datos")
# def enviar_datos():
#     global datos_recibidos, mensaje_recibido
#     # Si se ha recibido al menos un mensaje, devuelve los datos
#     # Si no, devuelve un mensaje indicando que aún no se ha recibido ningún dato
#     if mensaje_recibido:
#         return jsonify(datos_recibidos)
#     else:
#         return jsonify({"mensaje": "Aún no se han recibido datos"})

# def encodedMap_to_graph(rows, cols, mapa_code):
#     procesed = [mapa_code[i:i+2] for i in range(0, len(mapa_code), 2)]
#     G = nx.Graph()
#     G.add_nodes_from([i for i in range(len(procesed))])
    
#     # Por cada casilla del tablero
#     for i in range(len(procesed)):
#         # Calculo la casilla correspondiente
#         row = int(i/cols)
#         col = i%cols
#         c_arriba = ["02","03","06","07","08","10","11"]
#         c_abajo = ["02","04","05","08","09","10","11"]
#         c_derecha = ["01","03","04","07","08","09","11"]
#         c_izquierda = ["01","05","06","07","09","10","11"]
#         # Compruebo conexión arriba
#         if procesed[i] in c_arriba:
#             if row-1 >= 0:
#                 node = (row-1)*cols+col
#                 if procesed[node] != "00" and procesed[node] in c_abajo:
#                     G.add_edge(i, node)
#         # Compruebo conexión abajo
#         if procesed[i] in c_abajo:
#             if row+1 < rows:
#                 node = (row+1)*cols+col
#                 if procesed[node] != "00" and procesed[node] in c_arriba:
#                     G.add_edge(i, node)
#         # Compruebo conexión derecha
#         if procesed[i] in c_derecha:
#             if col+1 < cols:
#                 node = (row)*cols+col+1
#                 if procesed[node] != "00" and procesed[node] in c_izquierda:
#                     G.add_edge(i, node)
#         # Compruebo conexión izquierda
#         if procesed[i] in c_izquierda:
#             if col-1 >= 0:
#                 node = (row)*cols+col-1
#                 if procesed[node] != "00" and procesed[node] in c_derecha:
#                     G.add_edge(i, node)
#     return G

# def dijkstra(Graph, ini, fin):
#     return nx.dijkstra_path(Graph, ini, fin)

# def path_to_movement(path,cols,rows):
#     res = []
#     for i in range(len(path)-1):
        
#         dif = path[i]-path[i+1]
#         if dif==5:
#             pass
#         match dif:
#             case 1:
#                 res.append('left')
#             case -1:
#                 res.append('right')
#             case 5:
#                 res.append('up')
#             case _:
#                 res.append('down')
#     return res

# def delivery2movement(pick_pos,delivery_pos,initial_pos,graph):
#     to_pick = path_to_movement(path=dijkstra(Graph=graph,ini=initial_pos,fin=pick_pos),cols=cols,rows=rows)
#     to_pick.append('pick')
#     to_delivery = path_to_movement(path=dijkstra(Graph=graph,ini=pick_pos,fin=delivery_pos),cols=cols,rows=rows)
#     to_delivery.append('drop')
#     return to_pick+to_delivery

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify
from flask_mqtt import Mqtt

app = Flask(__name__)

app.config['MQTT_BROKER_URL'] = '10.82.146.13'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_PASSWORD'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_KEEPALIVE'] = 5  # Set KeepAlive time in seconds
app.config['MQTT_TLS_ENABLED'] = False  # If your broker supports TLS, set it True
topic = '/flask/mqtt'

mqtt_client = Mqtt(app)


@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe(topic) # subscribe topic
   else:
       print('Bad connection. Code:', rc)


@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
   data = dict(
       topic=message.topic,
       payload=message.payload.decode()
  )
   print('Received message on topic: {topic} with payload: {payload}'.format(**data))


@app.route('/publish', methods=['POST'])
def publish_message():
   request_data = request.get_json()
   publish_result = mqtt_client.publish(request_data['topic'], request_data['msg'])
   return jsonify({'code': publish_result[0]})

if __name__ == '__main__':
   app.run(host='127.0.0.1', port=5000)

