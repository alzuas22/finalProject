from flask import render_template, jsonify, request
from mycriptos import app
from mycriptos.models import *
import sqlite3

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
    


@app.route("/api/v1/tasa/<moneda_from>/<moneda_to>/<cantidad_from>", methods=["GET"])
def get_tasa(moneda_from, moneda_to, cantidad_from):
    try:
        if moneda_from != "EUR":
            
            saldo_disponible = verificar_saldo_suficiente(moneda_from)
            
            if float(saldo_disponible) >= float(cantidad_from) :
                tasa = obtener_tasa_de_cambio(moneda_from, moneda_to)
                return jsonify({"status": "success", "rate": tasa}), 201
            else:
                return jsonify({"status": "fail", "mensaje": "Saldo insuficiente"}), 400
            
            
            
    
        else: 
            tasa = obtener_tasa_de_cambio(moneda_from, moneda_to)
            return jsonify({"status": "success", "rate": tasa}), 201
    
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


# Ruta para crear un nuevo movimiento
@app.route("/api/v1/movimiento", methods=["POST"])
def crear_movimiento():
    try:
        data = request.get_json()  # Obtener los datos JSON de la solicitud
        moneda_from = data.get("moneda_from")
        cantidad_from = data.get("cantidad_from")
        moneda_to = data.get("moneda_to")
        cantidad_to = data.get("cantidad_to")
        
        movement = Movement(moneda_from, cantidad_from, moneda_to, cantidad_to)
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





