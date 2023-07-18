from datetime import datetime
import sqlite3

CURRENCIES = ("EUR", "BTC", "ETH", "USDT", "BNB", "XRP", "ADA", "SOL", "DOT", "MATIC")



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
        if self._cantidad_from == 0:
            raise ValueError("Amount must be positive or negative")
        
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
               (moneda_from, cantidad_from, moneda_to, cantidad_to)
        VALUES (?, ?, ?, ?)
        """

        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query, (movement.moneda_from, movement.cantidad_from,
                            movement.moneda_to, movement.cantidad_to))
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
