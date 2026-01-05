import sqlite3 as sql
from . import settings
from typing import Annotated

FechaFormatoDDMMYYYY = Annotated[str, "DD/MM/YYYY"]

class Database:
    def __init__(self):
        self.db = settings.db_path
        self.con = sql.connect(self.db)
        self.cur = self.con.cursor()
        #input("revisa la linea 12, que este bien la consulta sql")
        sql_query = """CREATE TABLE IF NOT EXISTS student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    fecha_nacimiento TEXT NOT NULL,
    rango REAL NOT NULL
);"""
        self.cur.execute(sql_query)
        self.con.commit()


    def fetch_all(self):
        self.cur.execute("SELECT * FROM student")
        rows = self.cur.fetchall()
        return rows
    
    def set(self,nombre: str,fecha_nacimiento: FechaFormatoDDMMYYYY ,rango: float):
        sql_query = """INSERT INTO student (nombre,fecha_nacimiento,rango) VALUES (?,?,?)"""
        try:
            self.cur.execute(sql_query,(nombre, fecha_nacimiento, rango))
            self.con.commit()
            return True
        except Exception:
            return False
        
    def update_by_id(self, id_: int, nombre: str, fecha_nacimiento: FechaFormatoDDMMYYYY, rango: float):
        sql_query = """UPDATE student SET nombre=?,fecha_nacimiento=?,rango=? WHERE id=?"""
        try:
            self.cur.execute(sql_query,(nombre, fecha_nacimiento, rango, id_))
            self.con.commit()
            return True
        except Exception:
            return False

    def delete_by_id(self, id_: int):
        sql_query = """DELETE FROM student WHERE id=?"""
        try:
            self.cur.execute(sql_query,(id_,))
            self.con.commit()
            return True
        except Exception:
            return False

    def get_by_name(self,name: str):
        # permite búsqueda parcial usando comodines
        like = f"%{name}%"
        self.cur.execute("SELECT * FROM student WHERE nombre LIKE ?", (like,))
        resultado = self.cur.fetchall()
        return resultado


    def get_by_id(self, id_: int):
        # buscar por id (código)
        self.cur.execute("SELECT * FROM student WHERE id = ?", (id_,))
        return self.cur.fetchall()



