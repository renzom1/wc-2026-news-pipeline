# Engineering Log

## Proyecto: World Cup 2026 News Pipeline

---

## Objetivo del proyecto

Queremos construir un pipeline de datos que recopile automáticamente noticias relacionadas con el Mundial 2026 y permita responder preguntas como:

- ¿Qué medios publican más noticias sobre el Mundial?
- ¿Cuántas noticias aparecen por día?
- ¿Qué noticias hablan de Argentina?

El objetivo principal no es obtener las noticias sino aprender:

- Data Engineering
- SQL
- Python aplicado a datos
- Diseño de pipelines

---

## ¿Qué es un pipeline?

Definimos un pipeline como:

```text
Datos crudos
     ↓
Extracción
     ↓
Transformación
     ↓
Almacenamiento
     ↓
Análisis
```

En nuestro caso:

```text
NewsAPI
    ↓
Python
    ↓
SQLite
    ↓
Consultas SQL
    ↓
Reportes
```

---

## Arquitectura elegida

```text
wc-news-pipeline/
│
├── database/
│   └── db.db
│
├── src/
│   └── test_api.py
│
└── README.md
```

### database/

Contiene la base de datos SQLite.

### src/

Contiene el código Python.

### README.md

Servirá para documentar:

- Qué hace el proyecto.
- Cómo ejecutarlo.
- Decisiones importantes de diseño.

---

## Diseño de la tabla raw_news

Creamos una tabla para almacenar las noticias descargadas.

```sql
CREATE TABLE raw_news (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    source TEXT,
    published_at TEXT,
    url TEXT UNIQUE,
    fetched_at TEXT
);
```

Posteriormente decidimos que probablemente agregaremos:

```sql
content TEXT
```

porque NewsAPI lo provee y podría resultar útil más adelante.

---

## Clave primaria vs URL

Discutimos dos conceptos diferentes.

### id

```sql
PRIMARY KEY
```

Es un identificador interno generado por SQLite.

Ejemplo:

```text
1
2
3
4
```

### url

```sql
UNIQUE
```

Es una regla de negocio.

Significa:

> No puede haber dos filas con la misma URL.

La URL no es la clave primaria.

---

## Duplicados e idempotencia

Planteamos el siguiente escenario:

### Día 1

```text
100 noticias
```

### Día 2

```text
95 repetidas
5 nuevas
```

Queremos:

```text
95 ignoradas
5 insertadas
```

Esto se llama:

### Idempotencia

Ejecutar varias veces el pipeline produce el mismo estado final.

---

## INSERT vs INSERT OR IGNORE

Probamos:

```sql
INSERT INTO ...
```

Resultado:

```text
UNIQUE constraint failed
```

porque la URL ya existía.

Luego usamos:

```sql
INSERT OR IGNORE ...
```

Resultado:

```text
duplicado
↓
se ignora
↓
el pipeline continúa
```

Aprendimos que:

> La base de datos protege la integridad.

No es Python quien detecta los duplicados.

---

## SQLite desde Python

Creamos una conexión:

```python
import sqlite3

conn = sqlite3.connect("../database/db.db")
```

Aprendimos que:

### conn

Es un objeto que representa una conexión entre Python y SQLite.

### conn.commit()

Guarda los cambios realizados.

### conn.close()

Cierra la conexión con la base de datos.

---

## Rutas relativas

Aprendimos por qué funciona:

```python
"../database/db.db"
```

porque Python busca el archivo respecto del directorio desde donde se ejecuta el script.

Visualmente:

```text
src/
 ↑
 │ ..
 │
database/
```

---

## Introducción a las APIs

Aprendimos que una API es una fuente de datos.

En nuestro pipeline:

```text
NewsAPI
      ↓
Python
      ↓
SQLite
```

La API cumple el mismo rol que una fuente experimental en Física.

---

## Endpoint

Elegimos:

```python
url = "https://newsapi.org/v2/everything"
```

Esto no contiene las noticias.

Es simplemente la dirección del servicio que vamos a consultar.

---

## Parámetros

Construimos:

```python
params = {
    "q": "World Cup 2026",
    "language": "en",
    "pageSize": 10,
    "apiKey": "..."
}
```

Aprendimos que:

> `params` representa el pedido que hacemos a la API.

No son noticias.

---

## requests.get()

Utilizamos:

```python
response = requests.get(url, params=params)
```

Conceptualmente:

```text
Python
  ↓
envía petición HTTP
  ↓
NewsAPI
  ↓
genera respuesta
  ↓
response
```

---

## ¿Qué es response?

Aprendimos que:

```python
response
```

no son las noticias.

Es un objeto que representa toda la respuesta enviada por el servidor.

Contiene:

- Status code.
- Headers.
- JSON.
- Metadatos de la respuesta.

---

## Verificación de la extracción

Usamos:

```python
print(response.status_code)
```

Obtuvimos:

```text
200
```

que significa:

> La comunicación con la API fue exitosa.

Primer éxito de la etapa **Extract**.

---

## JSON devuelto por NewsAPI

Utilizamos:

```python
response.json()
```

y observamos una estructura similar a:

```python
{
    "status": "ok",
    "totalResults": 100,
    "articles": [...]
}
```

Aprendimos:

```text
Diccionario principal
       ↓
articles
       ↓
Lista de noticias
       ↓
Cada noticia es otro diccionario
```

---

## Estructura de una noticia

Inspeccionamos:

```python
response.json()["articles"][0].keys()
```

y obtuvimos algo similar a:

```python
dict_keys([
    'source',
    'author',
    'title',
    'description',
    'url',
    'urlToImage',
    'publishedAt',
    'content'
])
```

---

## Primer ejemplo de transformación

Descubrimos que:

```python
article["source"]
```

no es un string.

Es:

```python
{
    "id": "the-verge",
    "name": "The Verge"
}
```

Por lo tanto decidimos almacenar:

```python
article["source"]["name"]
```

que produce:

```text
The Verge
```

---

## Mapeo NewsAPI → SQLite

| NewsAPI | raw_news |
|----------|----------|
| title | title |
| description | description |
| source["name"] | source |
| publishedAt | published_at |
| url | url |
| content | content (próximamente) |
| fecha actual | fetched_at |
| SQLite | id |

---

## Decisión sobre content

Discutimos los campos:

- `author`
- `content`

Conclusión:

- `author` no parece útil para nuestras preguntas actuales.
- `content` podría resultar útil para análisis futuros.

Por lo tanto, probablemente agregaremos:

```sql
content TEXT
```

a la tabla `raw_news`.

---

## Resumen conceptual

Estamos haciendo una petición HTTP GET a una API que devuelve un JSON.

Ese JSON se transforma en diccionarios y listas de Python para que posteriormente podamos:

1. Extraer los datos relevantes.
2. Transformarlos.
3. Insertarlos en SQLite.

Visualmente:

```text
NewsAPI
     ↓
HTTP GET
     ↓
JSON
     ↓
Python (dicts y listas)
     ↓
Transformación
     ↓
SQLite
```

---

## Estado actual del proyecto

Ya sabemos:

- ✅ Crear tablas SQLite.
- ✅ Conectar Python con SQLite.
- ✅ Insertar datos.
- ✅ Entender PRIMARY KEY.
- ✅ Entender UNIQUE.
- ✅ Entender idempotencia.
- ✅ Consumir una API real.
- ✅ Interpretar respuestas JSON.
- ✅ Inspeccionar estructuras de datos anidadas.
- ✅ Diseñar el mapeo entre origen y destino.

---

## Próximo paso

Construir la primera versión funcional de:

```text
EXTRACT
    +
LOAD
```

Es decir:

```text
NewsAPI
     ↓
response.json()
     ↓
extraer artículos
     ↓
transformarlos
     ↓
insertarlos en raw_news
```

A partir de ahí aparecerán conceptos importantes como:

- Iterar sobre una lista de artículos.
- Transformar campos.
- Generar `fetched_at`.
- Insertar múltiples noticias automáticamente.
- Verificar cuántas noticias fueron realmente almacenadas.

Será la primera vez que trabajemos con datos reales del Mundial 2026 en lugar de ejemplos inventados.