import sqlite3      #importamos sqlite3 desde Python (no es un paquete)

conn = sqlite3.connect("database/db.db")     #iniciamos la conexion entre Python y SQlite

cursor = conn.cursor()

url = None      #definimos variable url (https://espn.com/noticia1)

#insertamos noticia
cursor.execute("""        


INSERT OR IGNORE INTO raw_news (
    title,
    description,
    source,
    published_at,
    url,
    fetched_at
)
VALUES (
    'Julián Álvarez habla sobre el Mundial 2026',
    'Entrevista exclusiva',
    'ESPN',
    '2026-06-18',
    '',
    '2026-06-18'
)
""")
#todo lo que esta entre comillas es SQL, Python simplemente lo envia a SQLite


conn.commit()   #le decimos a SQLite “Confirmo todos los cambios desde el último commit”

print("Noticia insertada")

conn.close()    #cerramos conexion