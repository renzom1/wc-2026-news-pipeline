import requests

# URL del endpoint que queremos consultar.
# Un endpoint es una "puerta de entrada" específica de una API.
# En este caso usamos el endpoint "everything" de NewsAPI,
# que permite buscar artículos según distintos criterios.
url = "https://newsapi.org/v2/everything"


# Diccionario con los parámetros de búsqueda.
# Requests se encargará de convertirlos en una query string:
# ?q=World+Cup+2026&language=en&pageSize=10&apiKey=...
params = {

    # Palabras clave que NewsAPI utilizará para buscar noticias.
    # Cuanto más específica sea la búsqueda, más relevantes serán los resultados.
    "q": "World Cup 2026",

    # Idioma de las noticias devueltas.
    "language": "en",

    # Cantidad máxima de artículos a devolver.
    # Es útil para limitar el volumen de datos durante las pruebas.
    "pageSize": 10,

    # Clave personal de acceso a la API.
    # Funciona como una credencial que identifica quién realiza la consulta
    # y permite a NewsAPI controlar límites de uso y permisos.
    "apiKey": "662fe0534dae412f8700039bf16b10cc"
}


# Enviamos una petición HTTP GET al servidor de NewsAPI.
#
# Conceptualmente:
# Cliente (nuestro script) ---> Servidor (NewsAPI)
#
# Requests agrega automáticamente los parámetros a la URL,
# envía la solicitud y guarda la respuesta en el objeto 'response'.
response = requests.get(url, params=params)


# Imprime una representación simple de la respuesta.
# Por ejemplo: <Response [200]>
# El código 200 significa que la petición fue exitosa.
print(response)


# Devuelve únicamente el código de estado HTTP.
# Algunos códigos comunes:
# 200 -> éxito
# 401 -> API Key inválida
# 429 -> límite de consultas excedido
# 500 -> error del servidor
# print(response.status_code)


# Convierte el JSON recibido desde la API en un diccionario de Python.
# Muy útil para inspeccionar toda la estructura de la respuesta.
# print(response.json())


# Muestra las claves principales del JSON devuelto.
# Por ejemplo:
# dict_keys(['status', 'totalResults', 'articles'])
#
# Esto ayuda a explorar una API nueva.
# print(response.json().keys())


# 'articles' es una lista de noticias.
# [0] selecciona la primera noticia.
# .keys() muestra todos los campos disponibles para esa noticia.
#
# Ejemplo:
# dict_keys(['source', 'author', 'title', 'description', ...])
# print(response.json()["articles"][0].keys())


# Accedemos al campo 'source' de la primera noticia.
#
# Estructura conceptual:
#
# response.json()
# └── articles (lista)
#      ├── noticia 0 (diccionario)
#      │     ├── source
#      │     ├── title
#      │     ├── url
#      │     └── ...
#      └── noticia 1
#
# En este caso imprimimos el diccionario completo asociado a 'source'.
# Normalmente contiene algo como:
# {'id': 'bbc-news', 'name': 'BBC News'}
print(response.json()["articles"][0]["source"])