from datetime import datetime
from mycriptos import app
import sqlite3
from dotenv import load_dotenv
import requests, os
from flask import jsonify

CURRENCIES = ("EUR", "BTC", "ETH", "USDT", "BNB", "XRP", "ADA", "SOL", "DOT", "MATIC")

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la API KEY de CoinAPI.io desde las variables de entorno
API_KEY = os.getenv("API_KEY")

def obtener_tasa_de_cambio(moneda_from, moneda_to):
    try:
        # URL de la API utilizando los parámetros proporcionados y API KEY
        url = f"https://rest.coinapi.io/v1/exchangerate/{moneda_from}/{moneda_to}?apikey={API_KEY}"

        # Realiza una solicitud GET a CoinAPI.io con tu API KEY
        response = requests.get(url)

        # Verifica si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            # Analiza los datos JSON de la respuesta
            data = response.json()

            # Extrae el valor de la tasa de cambio de los datos de la respuesta
            rate = data.get("rate")

            # Devuelve la tasa de cambio
            return rate
        else:
            raise ValueError(f"Error al obtener la tasa de cambio ({response.status_code}): {response.text}")

    except requests.exceptions.RequestException as e:
        # Si ocurrió un error durante la solicitud, muestra un mensaje de error
        raise ValueError(f"Error en la solicitud: {e}")

def verificar_saldo_suficiente(moneda_buscada):
    try:        
        query1 = """
        SELECT SUM(cantidad_to) FROM movements WHERE moneda_to = ?;
        """
        query2 = """
        SELECT SUM(cantidad_from) FROM movements WHERE moneda_from = ?;
        """

        conn = sqlite3.connect(app.config.get("PATH_SQLITE"))
        cur = conn.cursor()
        cur.execute(query1, (moneda_buscada,))
        suma_cantidades_to = cur.fetchone()[0] 
        cur.execute(query2, (moneda_buscada,))
        suma_cantidades_from = cur.fetchone()[0] or 0.0
        conn.close()
        saldo = suma_cantidades_to - suma_cantidades_from
        return saldo   
        
    except sqlite3.Error as e:
        raise ValueError(f"Error en la consulta a la base de datos: {e}")


def obtener_monedas_disponibles(moneda_from, cantidad_moneda_to):
    try:
        # Lista de monedas disponibles que cumplen la condición
        monedas_disponibles = []

        # Obtener el saldo total de cada moneda_from y sus tasas de cambio con EUR
        with sqlite3.connect(app.config.get("PATH_SQLITE")) as conn:
            cursor = conn.cursor()
             # Cantidad total de moneda_from
            cursor.execute("SELECT SUM(cantidad_to) FROM movements WHERE moneda_to = ?", (moneda_from,))
            cantidad_mimoneda = cursor.fetchone()[0]  # Obtenemos el resultado de la suma

            # Obtener la tasa de cambio entre moneda_from y EUR
            tasa_1 = obtener_tasa_de_cambio(moneda_from, "EUR")
            
            for moneda in CURRENCIES:
                # Obtener la tasa de cambio entre moneda_to y EUR
                tasa_2 = obtener_tasa_de_cambio(moneda, "EUR")

                # Verificar si cumple la condición y agregar a la lista de monedas disponibles
                if cantidad_mimoneda * tasa_1 >= cantidad_moneda_to * tasa_2:
                    monedas_disponibles.append(moneda_from)

        return monedas_disponibles

    except sqlite3.Error as e:
        print(f"Error en la consulta a la base de datos: {e}")
        return []






class Movement:
    def __init__(self, moneda_from, cantidad_from, moneda_to, cantidad_to, id = None):
        self.date = datetime.now().strftime('%Y-%m-%d')
        self.id = id
        self.time = datetime.now().strftime('%H:%M:%S')
        self.moneda_from = moneda_from
        self.cantidad_from = cantidad_from
        self.moneda_to = moneda_to
        self.cantidad_to = cantidad_to
       
    @property
    def cantidad_from(self):
        return self._cantidad_from
    
    @cantidad_from.setter
    def cantidad_from(self, value):
        self._cantidad_from = float(value)
        if self._cantidad_from <= 0:
            raise ValueError("Amount must be positive ")
        
    @property
    def moneda_from(self):
        return self._moneda_from
    
    @moneda_from.setter
    def moneda_from(self, value):
        self._moneda_from = value
        if self._moneda_from not in CURRENCIES:
            raise ValueError(f"currency must be in {CURRENCIES}")
        
    @property
    def moneda_to(self):
        return self._moneda_to
    
    @moneda_to.setter
    def moneda_to(self, value):
        self._moneda_to = value
        if self._moneda_to not in CURRENCIES:
            raise ValueError(f"currency must be in {CURRENCIES}")

    def to_dict(self):
        return {
            "id": self.id,
            "date": str(self.date),
            "time": self.time,
            "moneda_from": self.moneda_from,
            "cantidad_from": self.cantidad_from,
            "moneda_to": self.moneda_to,
            "cantidad_to": self.cantidad_to
        }
    
class MovementDAOsqlite:
    def __init__(self, db_path):
        self.path = db_path 

        query = """
        CREATE TABLE IF NOT EXISTS "movements" (
	"id"	INTEGER UNIQUE,
	"date"	TEXT NOT NULL,
	"time"	TEXT NOT NULL,
	"moneda_from"	TEXT NOT NULL,
	"cantidad_from"	REAL NOT NULL,
    "moneda_to"	TEXT NOT NULL,
	"cantidad_to"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
        """
        
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query)
        conn.close()

    def insert(self, movement):

        query = """
        INSERT INTO movements
               (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to)
        VALUES (?, ?, ?, ?, ?, ?);
        """

        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query, (movement.date, movement.time, movement.moneda_from, 
                            movement.cantidad_from, movement.moneda_to, movement.cantidad_to))
        conn.commit()
        conn.close()

    def get(self, id):
        query = """
        SELECT date, time, moneda_from, cantidad_from, moneda_to, cantidad_to, id
          FROM movements
         WHERE id = ?;
        """
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query, (id,))
        res = cur.fetchone()
        conn.close()
        if res:
            return Movement(*res)

        
    def get_all(self):
        query = """
        SELECT date, time, moneda_from, cantidad_from, moneda_to, cantidad_to, id
          FROM movements
         ORDER by date;
        """
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query)
        res = cur.fetchall()
        
        lista = []
        for reg in res:
            lista.append(
                {
                    "date": reg[0],
                    "time": reg[1],
                    "moneda_from": reg[2],
                    "cantidad_from": reg[3],
                    "moneda_to": reg[4],
                    "cantidad_to": reg[5],
                    "id": reg[6]
                }
            )

        conn.close()
        return lista
