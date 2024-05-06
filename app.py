from flask import Flask, request
from flask_mqtt import Mqtt

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'http://test.mosquitto.org'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'user'
app.config['MQTT_PASSWORD'] = 'password'

mqtt = Mqtt()

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    mqtt.subscribe('topic/test')

@mqtt.on_message()
def handle_message(client, userdata, message):
    print("Received message '" + str(message.payload) + "' on topic '" + message.topic + "'")

@app.route('/enviarSalidaLlegada', methods=['POST'])
def send_message():
    topic = request.form.get('topic')
    message = request.form.get('message')
    mqtt.publish(topic, message)
    return 'Message sent to topic: ' + topic

if __name__ == '__main__':
    mqtt.init_app(app)
    app.run()

import routes