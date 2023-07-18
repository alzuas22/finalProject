from flask import render_template, jsonify, request
import requests
from mycriptos import app
from mycriptos.models import Movement, MovementDAOsqlite

dao = MovementDAOsqlite(app.config.get("PATH_SQLITE"))

# Ruta para servir la página principal
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/v1/all")
def todos():
    movements = dao.get_all()
    return movements