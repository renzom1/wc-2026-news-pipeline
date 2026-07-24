# NewsAPI

## Endpoint utilizado

https://newsapi.org/v2/everything

## Parámetros de búsqueda

| Parámetro | Descripción |
|-----------|-------------|
| apiKey | Credencial |
| q | Término de búsqueda |
| language | Idioma |
| pageSize | Cantidad de resultados |
| page | Página |
| sortBy | Orden |
| from | Fecha mínima |
| to | Fecha máxima |


## Flujo de una consulta a NewsAPI

Primero definimos el endpoint de NewsAPI:

```python
url = "https://newsapi.org/v2/everything"
```

Esta URL no contiene las noticias, sino que indica el servicio de NewsAPI al que queremos hacer la consulta.

Luego definimos un diccionario llamado `params`, que contiene los parámetros de búsqueda elegidos por nosotros:

```python
params = {
    "q": "World Cup 2026",
    "language": "en",
    "pageSize": 10,
    "apiKey": "..."
}
```

Este diccionario representa el pedido que queremos hacer a la API. En este caso, estamos solicitando hasta 10 noticias en inglés relacionadas con `"World Cup 2026"`, identificándonos mediante nuestra API key.

A continuación ejecutamos:

```python
response = requests.get(url, params=params)
```

Con esta instrucción, Python envía una petición HTTP al servidor de NewsAPI utilizando el endpoint especificado y los parámetros definidos en `params`.

El servidor recibe la petición, busca en su base de datos las noticias que cumplen las condiciones solicitadas y genera una respuesta. Esa respuesta queda almacenada en la variable `response`.

Es importante notar que `response` no contiene directamente las noticias, sino un objeto especial de la librería `requests` que representa la respuesta completa del servidor.

Este objeto contiene información como:

- El código de estado de la petición.
- Las cabeceras de la respuesta.
- Los datos devueltos por la API.

Posteriormente podremos extraer esos datos mediante métodos como:

```python
response.json()
```

Este método convierte la respuesta JSON enviada por NewsAPI en estructuras de datos de Python (principalmente diccionarios y listas), permitiéndonos analizarlas, transformarlas y almacenarlas posteriormente en nuestra base de datos SQLite.