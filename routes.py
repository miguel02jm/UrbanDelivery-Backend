from app import app
from flask import jsonify

@app.route("/InteligenciaAmbiental/datos")
def enviar_datos():
    datos = [1, 2, 3, 4, 5]
    return jsonify(datos)