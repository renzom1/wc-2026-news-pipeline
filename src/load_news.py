#importamos paquetes y  librerias
import requests
import json
import sqlite3      #importamos sqlite3 desde Python (no es un paquete)
from datetime import datetime, UTC, timedelta
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
import os
import smtplib
from email.message import EmailMessage


#configuracion. cargamos informacion
load_dotenv()
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")


#obtener_noticias() 
def obtener_noticias(query, desde, hasta):
    url_api = "https://newsapi.org/v2/everything"
    params = {                  #determinamos parametros que correspondan a las noticias del mundial
    "q": query,                  
    "language": "en",
    "pageSize": 10,
    "apiKey": NEWS_API_KEY,    #apiKey seria nuestro "usuario" para pedirle cosas a la API
    "from": desde.isoformat(),
    "to": hasta.isoformat(),
    "sortBy": "publishedAt"
}
    response = requests.get(url_api, params=params)
    
    if response.status_code == 200:
        articles = response.json()['articles']
        return articles
        
    else:
        raise ConnectionError("No se pudieron obtener las noticias.")
#Fin obtener_noticias()


#Empieza guardar_noticias()
def guardar_noticias(lista_noticias, fetched_at):
    
    conn = sqlite3.connect("database/db.db")   
    cursor = conn.cursor() 

    urls_guardadas = []

    for article in lista_noticias:
        title = article['title']
        source = article['source']['name']
        description = article['description']
        published_at = article['publishedAt']
        url_article = article['url']
        
        
        tupla_valores = (
            title,
            description,
            source,
            published_at,
            url_article,
            fetched_at
        )  
                  
                  
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
        
                   
        if cursor.rowcount == 1:        #es un atributo del cursor que indica cuántas filas fueron afectadas por la última sentencia SQL que ejecute con ese cursor.
            urls_guardadas.append(url_article)
        
    conn.commit()   
    conn.close()            
    return urls_guardadas  
#Fin guardar_noticias()


#Empieza preparar_correo()
def preparar_correo(lista_urls):
        msg = EmailMessage()
        msg['From'] = GMAIL_USER
        msg['To'] = GMAIL_USER
        msg['Subject'] = 'Noticias de hoy'
        cuerpo_mail = '\n'.join(lista_urls)
        msg.set_content(cuerpo_mail)
        return msg
#Fin preparar_correo()


#Empieza enviar_correo()
def enviar_correo(mensaje):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(GMAIL_USER, GMAIL_PASSWORD)
    server.send_message(mensaje)
    server.quit()
#Fin enviar_correo()


#creamos main, encargada de organizar el flujo del pipeline.
def main():
    zona_local = ZoneInfo("America/Argentina/Buenos_Aires")
    hasta = datetime.now(zona_local)
    desde = hasta - timedelta(hours=48)
    fetched_at = hasta.isoformat()
    noticias = obtener_noticias("World Cup", desde, hasta)
    urls_guardadas = guardar_noticias(noticias, fetched_at)
    
    if urls_guardadas:      #no hace falta poner if(len(lista)) porque python toma listas como true(no vacia) o false(vacia)
        msg = preparar_correo(urls_guardadas)
        enviar_correo(msg)
        
#condicion para que se ejecute el script, sin esto quedan guardadas las funciones pero no corre el flujo
if __name__ == "__main__":  #si no esta este if y algun dia hago import load_news, todo el script se ejecutaria automaticamente, y capaz no quiero eso sino solo usar alguna funcion de este archivo
    main()