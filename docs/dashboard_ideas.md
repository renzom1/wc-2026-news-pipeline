# Dashboard Ideas

## Objetivo

Construir un dashboard en Power BI que permita analizar tanto las noticias almacenadas por el pipeline como el comportamiento del propio pipeline.

El objetivo no es solamente aprender Power BI, sino también identificar mejoras en el diseño del pipeline y del modelo de datos a medida que surgen nuevas necesidades de análisis.

---

# Preguntas que el modelo actual puede responder

## Noticias

- ¿Qué fuentes publican más noticias?
- ¿Cómo se distribuyen las noticias por fuente en un período determinado?
- ¿Cuántas noticias fueron insertadas en cada ejecución del pipeline? *(utilizando `fetched_at` como identificador de facto de la ejecución)*
- ¿Cómo evoluciona la cantidad acumulada de noticias almacenadas?

---

# Preguntas que el modelo actual NO puede responder

## Pipeline

- ¿Cuántas noticias devolvió NewsAPI en cada ejecución?
- ¿Cuántas noticias fueron descartadas por duplicadas?
- ¿Qué porcentaje de las noticias obtenidas fueron realmente nuevas?
- ¿Cuánto tiempo tardó cada ejecución?
- ¿Hubo errores durante una ejecución?
- ¿Cuántas ejecuciones fallaron?

---

# Posibles mejoras del pipeline

Estas mejoras no se implementarán inmediatamente. Se incorporarán únicamente cuando una necesidad de análisis las justifique.

## Tabla `pipeline_runs`

Posibles campos:

- run_id
- execution_time
- execution_end_time
- duration_seconds
- articles_received
- articles_inserted
- duplicates
- execution_status

La tabla `raw_news` podría incorporar un `run_id` como clave foránea para relacionar cada noticia con la ejecución en la que fue insertada.

---

# Notas de diseño

- `published_at` representa el momento en que la noticia fue publicada por el medio.
- `fetched_at` representa el momento en que el pipeline descargó la noticia.
- Actualmente `fetched_at` funciona como un identificador implícito de la ejecución, ya que todas las noticias insertadas en una misma corrida comparten el mismo timestamp.
- En una versión futura sería preferible utilizar una tabla específica para representar las ejecuciones del pipeline.