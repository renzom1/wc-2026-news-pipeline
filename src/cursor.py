import sqlite3

conn = sqlite3.connect("../database/db.db")

cursor = conn.cursor() # intermediario que envia ordenes SQL a la base de datos  