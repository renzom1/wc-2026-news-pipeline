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


---

# Evolución del proyecto

## Primera versión funcional

La primera versión funcional del pipeline tenía un flujo secuencial dentro del script principal:

```text
Obtención de noticias
        ↓
Procesamiento
        ↓
Inserción en SQLite
        ↓v     
Preparación del correo
        ↓
Envío
```




## Refactorización del pipeline

### Situación inicial

La primera versión del script tenía un flujo completamente secuencial: las instrucciones se ejecutaban a medida que Python recorría el archivo.

Aunque funcionaba, dificultaba la organización y la reutilización del código.

---

### Decisión tomada

Se reorganizó el pipeline separando responsabilidades en funciones:

```text
obtener_noticias()
        ↓
guardar_noticias()
        ↓
preparar_correo()
        ↓
enviar_correo()
```


---

## Incorporación de main()

Luego de la refactorización se incorporó una función principal:

```python
def main():
```

encargada de coordinar el flujo completo del pipeline.

Conceptualmente:

```text
main()

    ↓

configuración del entorno

    ↓

extracción de noticias

    ↓

almacenamiento

    ↓

decisión de envío de correo
```

La función `main()` funciona como punto central de coordinación, mientras que las demás funciones contienen la lógica específica de cada etapa.

---

## Punto de entrada del programa

Se incorporó:

```python
if __name__ == "__main__":
    main()
```

Este bloque permite diferenciar entre dos formas de utilizar el archivo Python.

### Ejecución directa

Cuando el archivo se ejecuta directamente:

```bash
python src/load_news.py
```

se inicia el pipeline completo mediante la llamada a:

```python
main()
```

---

### Importación como módulo

Si el archivo es importado:

```python
import load_news
```

Python carga las funciones disponibles, pero no ejecuta automáticamente el pipeline.

Esto permite reutilizar funciones individuales sin iniciar todo el flujo de procesamiento.

---

## Gestión de credenciales mediante variables de entorno

Se incorporó el uso de variables de entorno mediante `python-dotenv`.

Las credenciales sensibles:

```text
NEWS_API_KEY
GMAIL_USER
GMAIL_PASSWORD
```

se almacenan fuera del código fuente.

El archivo:

```text
.env
```

contiene los valores reales, mientras que:

```text
.env.example
```

funciona como plantilla para indicar las variables necesarias para ejecutar el proyecto.

Esta separación permite:

- evitar exponer información sensible;
- facilitar la configuración por otros usuarios;
- mantener configuraciones diferentes según el entorno.

---

## Automatización del pipeline

El pipeline fue configurado para ejecutarse automáticamente mediante Windows Task Scheduler.

La tarea programada utiliza:

- el intérprete de Python perteneciente al entorno virtual del proyecto;
- el script principal del pipeline.

Flujo conceptual:

```text
Windows Task Scheduler

        ↓

Entorno virtual Python

        ↓

Pipeline ETL

        ↓

SQLite + Email
```

La automatización permite ejecutar el proceso diariamente sin intervención manual.

---

## Estado actual del proyecto

Actualmente el pipeline permite:

- ✅ Consumir una API REST real.
- ✅ Procesar respuestas JSON.
- ✅ Extraer campos relevantes de noticias.
- ✅ Transformar datos antes del almacenamiento.
- ✅ Guardar información en SQLite.
- ✅ Evitar duplicados mediante restricciones UNIQUE.
- ✅ Implementar inserciones idempotentes.
- ✅ Gestionar credenciales mediante variables de entorno.
- ✅ Separar responsabilidades mediante funciones.
- ✅ Automatizar la ejecución del pipeline.

---

## Próximos pasos

Las siguientes mejoras previstas son:

- Incorporar logging estructurado.
- Mejorar manejo de excepciones.
- Agregar pruebas automatizadas.
- Dockerizar el pipeline.
- Migrar SQLite a PostgreSQL.
- Desplegar el pipeline en un entorno cloud.
- Incorporar consultas SQL para análisis de noticias.
