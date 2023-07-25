from flask import render_template, jsonify
from mycriptos import app
from mycriptos.models import *
import requests, sqlite3

dao = MovementDAOsqlite(app.config.get("PATH_SQLITE"))

# Ruta para servir la página principal
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/v1/movimientos", methods=["GET"])
def get_movimientos():
    try:
        movements = dao.get_all()
        response = {
            "status": "success",
            "data": movements
        }
        return response
    except sqlite3.Error as e:
        response = {
            "status": "fail",
            "data": str(e)
        }
        return response, 400
    


@app.route("/api/v1/tasa/<moneda_from>/<moneda_to>", methods=["GET"])
def get_tasa(moneda_from, moneda_to):
    # Verifica si moneda_from no es EUR
    if moneda_from != "EUR":
        # Verifica si existe saldo suficiente antes de grabar el movimiento
        # Aquí debes agregar la lógica para verificar el saldo
        saldo_suficiente = verificar_saldo_suficiente(moneda_from)

        if not saldo_suficiente:
            # Si no hay saldo suficiente, devuelve un JSON con status "fail" y mensaje de error
            return jsonify({"status": "fail", "mensaje": "Saldo insuficiente"}), 400
        else: 
            tasa = obtener_tasa_de_cambio(moneda_from, moneda_to)
            monedas_disponibles = obtener_monedas_disponibles()
            return jsonify({"status": "success", "rate": tasa, "monedas": monedas_disponibles}), 201
    
    else: 
        tasa = obtener_tasa_de_cambio(moneda_from, moneda_to)
        monedas_disponibles = obtener_monedas_disponibles()
        return jsonify({"status": "success", "rate": tasa, "monedas": monedas_disponibles}), 201


# Ruta para crear un nuevo movimiento
@app.route("/api/v1/movimiento", methods=["POST"])
def crear_movimiento():
    try:
        movement = Movement(requests.json.get("date"),
                            requests.json.get("time"),
                            requests.json.get("moneda_from"),
                            requests.json.get("cantidad_from"),
                            requests.json.get("moneda_to"),
                            requests.json.get("cantidad_to"))
        
        dao.insert(movement)
        response = {
            "status": "success",
            "data": None
        }
        return response
    except ValueError as e:
        response = {
            "status": "fail",
            "data": str(e)
        }
        return response, 400
    except sqlite3.Error as e:
        response = {
            "status": "fail",
            "data": "Error en base de datos."
        }
        return response, 400


# Ruta para obtener el estado de la inversión
@app.route("/api/v1/status")
def get_status():
    pass
    # Lógica para obtener el estado de la inversión y formatear la respuesta





