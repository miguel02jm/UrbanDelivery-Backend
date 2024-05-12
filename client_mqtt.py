from flask_mqtt import Mqtt
from app import app
from variables import mqtt_messages

app.config['MQTT_BROKER_URL'] = '192.168.1.151'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
topic = '/GrupoP/ruta'
topic2 = '/map'

mqtt_client = Mqtt(app)

@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe(topic)
       mqtt_client.subscribe(topic2)
   else:
       print('Bad connection. Code:', rc)