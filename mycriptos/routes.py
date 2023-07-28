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
        if float(cantidad_from) <= 0:
            return jsonify({"status": "fail", "data": "La cantidad debe ser positiva"}), 400
    
        if moneda_from != "EUR":
            
            saldo_disponible = verificar_saldo_suficiente(moneda_from)
            
            if float(saldo_disponible) >= float(cantidad_from) :
                tasa = obtener_tasa_de_cambio(moneda_from, moneda_to)
                return jsonify({"status": "success", "rate": tasa}), 201
            else:
                return jsonify({"status": "fail", "data": "Saldo insuficiente"}), 400        
    
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
    try:
        # Get all movements from the database
        movements = dao.get_all()

        unique_currencies_to = get_unique_currencies_to(movements)
        unique_currencies_from = get_unique_currencies_from(movements)
        currency_totals_to = get_sum_by_currency_to(movements, unique_currencies_to)
        currency_totals_from = get_sum_by_currency_from(movements, unique_currencies_from)
        currency_totals_dict_to = dict(zip(unique_currencies_to, currency_totals_to))
        currency_totals_dict_from = dict(zip(unique_currencies_from, currency_totals_from))
        resultado = {moneda: currency_totals_dict_to.get(moneda, 0) - currency_totals_dict_from.get(moneda, 0) for moneda in set(currency_totals_dict_to) | set(currency_totals_dict_from)}

        price = resultado["EUR"]

        # Primero, inicializamos response_data con un wallet vacío.
        response_data = {
            "wallet": {},
            "price":price,
        }

        # Llenamos wallet
        for moneda, balance in resultado.items():
            response_data["wallet"][moneda] = {
                "balance": balance,
                "value": balance * obtener_tasa_de_cambio(moneda, "EUR")
            }

        # Ahora que tenemos el wallet lleno, podemos calcular actual_value.
        actual_value = 0
        for moneda, datos in response_data["wallet"].items():
            if moneda != "EUR":
                actual_value += datos["value"]

        # Finalmente, añadimos actual_value a response_data.
        response_data["actual_value"] = actual_value  

        # Return the data as a JSON response
        return jsonify({"status": "success", "data": response_data}), 200

    except ValueError as e:
        response = {"status": "fail", "data": str(e)}
        return response, 400
    except sqlite3.Error as e:
        response = {"status": "fail", "data": "Error en base de datos"}
        return response, 400



