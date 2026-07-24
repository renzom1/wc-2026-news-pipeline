# Notas de Data Engineering

## Diseño de proyectos de Data Engineering

Un proyecto de Data Engineering empieza por pensar en las preguntas que queremos que nuestro sistema responda.

---

## Conexión entre Python y SQLite

`conn` es un objeto que representa una conexión abierta entre Python y la base de datos SQLite. Gracias a esta conexión, Python puede comunicarse con la base de datos.

---

## Inserción de datos en SQL

`INSERT INTO` inserta una fila en una tabla.

Ejemplo:

```sql
INSERT INTO raw_news (title, author)
VALUES ('Título de ejemplo', 'Autor');
```

---

## ¿Qué hace `conn.commit()`?

Con `conn.commit()` le decimos a SQLite:

> "Confirmo todos los cambios realizados desde el último commit."

Por ejemplo:

```python
cursor.execute("INSERT noticia 1")
cursor.execute("INSERT noticia 2")
cursor.execute("INSERT noticia 3")
```

Hasta que no ejecutemos:

```python
conn.commit()
```

los cambios podrían existir solamente en memoria y no estar guardados permanentemente en la base de datos.

Puede pensarse como una especie de **firma** o **confirmación definitiva** de los cambios realizados.

---

## Modificar estructuras existentes en SQL

En SQL, modificar una estructura existente mediante `ALTER TABLE` suele ser más delicado porque hay que respetar los datos que ya están almacenados.

Además, las restricciones (*constraints*) no son simplemente documentación: la base de datos las verifica activamente.

Por ejemplo:

```sql
ALTER TABLE raw_news
ADD CONSTRAINT unique_title UNIQUE(title);
```

En este caso, la base de datos comprobará que no existan valores duplicados en la columna correspondiente.

---

## Pipeline idempotente

Un pipeline **idempotente** es un flujo de datos que produce exactamente el mismo resultado final, sin importar cuántas veces se ejecute.

En otras palabras:

- Ejecutarlo una vez → resultado correcto.
- Ejecutarlo dos veces → mismo resultado.
- Ejecutarlo diez veces → mismo resultado.

La ejecución repetida no genera duplicados ni inconsistencias.

---

## Restricciones y responsabilidades

Las restricciones de los datos pertenecen a la **base de datos**, no a la aplicación.

La aplicación puede intentar validar datos, pero la última línea de defensa debe estar en la base de datos mediante restricciones como:

- `PRIMARY KEY`
- `UNIQUE`
- `NOT NULL`
- `FOREIGN KEY`
- `CHECK`

De esta forma, la integridad de los datos queda garantizada independientemente de qué aplicación acceda a la base de datos.

## response.json()

Convierte el JSON recibido en estructuras de Python.

## JSON

Formato estándar para intercambiar datos.

## json.dumps()

Convierte estructuras de Python en texto JSON.