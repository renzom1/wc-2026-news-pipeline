# Dashboard Ideas

## Objetivo

Construir un dashboard en Power BI que permita analizar tanto las noticias almacenadas por el pipeline como el comportamiento del propio pipeline.

El objetivo no es solamente aprender Power BI, sino también identificar mejoras en el diseño del pipeline y del modelo de datos a medida que surgen nuevas necesidades de análisis.

---

# Preguntas que el modelo actual puede responder

## Noticias

* ¿Qué fuentes publican más noticias?

* ¿Cómo se distribuyen las noticias por fuente en un período determinado?

* ¿Cuántas noticias fueron insertadas en cada ejecución del pipeline?

  Actualmente se utiliza `fetched_at_norm` como identificador implícito de la ejecución, ya que todas las noticias insertadas en una misma corrida comparten el mismo timestamp.

* ¿Cómo evoluciona la cantidad acumulada de noticias almacenadas?

  Se resolvió mediante una medida DAX (`Accumulated News`) que calcula la cantidad acumulada de noticias hasta cada ejecución del pipeline.

  La lógica consiste en:

  * Obtener la ejecución actual a partir de `MAX(fetched_at_norm)`.
  * Ignorar el filtro aplicado por el eje temporal del gráfico.
  * Filtrar todas las noticias cuya ejecución sea menor o igual a la ejecución actual.
  * Contar las noticias resultantes.

  Para esto fue necesario utilizar `ALL(raw_news)` dentro de `FILTER`, ya que de otro modo el filtro del gráfico limitaba la tabla únicamente a la ejecución actual y no permitía recuperar ejecuciones anteriores.

---

# Preguntas que el modelo actual NO puede responder

## Pipeline

* ¿Cuántas noticias devolvió NewsAPI en cada ejecución?
* ¿Cuántas noticias fueron descartadas por duplicadas?
* ¿Qué porcentaje de las noticias obtenidas fueron realmente nuevas?
* ¿Cuánto tiempo tardó cada ejecución?
* ¿Hubo errores durante una ejecución?
* ¿Cuántas ejecuciones fallaron?

Estas preguntas requieren información sobre la ejecución del pipeline, no solamente sobre las noticias insertadas.

---

# Posibles mejoras del pipeline

Estas mejoras no se implementarán inmediatamente. Se incorporarán únicamente cuando una necesidad de análisis las justifique.

## Tabla `pipeline_runs`

Posibles campos:

* run_id
* execution_time
* execution_end_time
* duration_seconds
* articles_received
* articles_inserted
* duplicates
* execution_status

La tabla `raw_news` podría incorporar un `run_id` como clave foránea para relacionar cada noticia con la ejecución en la que fue insertada.

Esto permitiría responder preguntas sobre el comportamiento del pipeline sin tener que inferir ejecuciones a partir de los timestamps de las noticias.

---

# Notas de diseño

* `published_at` representa el momento en que la noticia fue publicada por el medio.
* `fetched_at_norm` representa el momento en que el pipeline descargó la noticia.
* Actualmente `fetched_at_norm` funciona como un identificador implícito de la ejecución, ya que todas las noticias insertadas en una misma corrida comparten el mismo timestamp.
* En una versión futura sería preferible utilizar una tabla específica para representar las ejecuciones del pipeline.

---

# Notas sobre medidas DAX

Las métricas analíticas se implementan mediante medidas DAX en Power BI, evitando modificar la base de datos para cada nueva pregunta.

Ejemplos desarrollados:

## News Count

Cantidad de noticias insertadas:

```DAX
News Count = COUNT(raw_news[url])
```

## Accumulated News

Cantidad acumulada de noticias a lo largo de las ejecuciones.

Durante su implementación se observó la importancia del contexto de filtro en DAX:

* Un visual de Power BI aplica filtros automáticamente según los campos utilizados en los ejes.
* `FILTER(raw_news, ...)` trabaja sobre la tabla ya filtrada por el contexto actual.
* Para cálculos acumulativos es necesario partir de una tabla sin ese filtro temporal mediante `ALL(raw_news)`.

Conceptualmente:

1. Obtener la ejecución actual.
2. Recuperar todas las noticias ignorando el filtro del gráfico.
3. Conservar únicamente las noticias correspondientes a ejecuciones anteriores o iguales.
4. Contar las filas resultantes.

Este patrón será útil para futuros análisis temporales dentro del dashboard.
