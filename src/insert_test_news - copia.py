import sqlite3      #importamos sqlite3 desde Python (no es un paquete)

conn = sqlite3.connect("database/db.db")     #iniciamos la conexion entre Python y SQlite

cursor = conn.cursor()


tupla_valores = (
    'Messi',
    'Messi mete un hattrick',
    'ESPN',
    '2026-06-18',
    None,
    '2026-06-18'
)

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
    ?,
    ?,
    ?,
    ?,
    ?,
    ?
)
""", tupla_valores
)
#todo lo que esta entre comillas es SQL, Python simplemente lo envia a SQLite


conn.commit()   #le decimos a SQLite “Confirmo todos los cambios desde el último commit”

print("Noticia insertada")

conn.close()    #cerramos conexion