import requests
import json
import sqlite3      #importamos sqlite3 desde Python (no es un paquete)
from datetime import datetime, UTC, timedelta
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
import os
import smtplib
from email.message import EmailMessage



load_dotenv()
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")



#obtener_noticias() 
def obtener_noticias(query, desde, hasta):
    url_api = "https://newsapi.org/v2/everything"
    params = {                                          #determinamos parametros que correspondan a las noticias del mundial
    "q": query,                  
    "language": "en",
    "pageSize": 10,
    "apiKey": NEWS_API_KEY,    #apiKey seria nuestro "usuario" para pedirle cosas a la API
    "from": desde.isoformat(),
    "to": hasta.isoformat(),
    #"from" : "2026-07-16T00:00:00",
    #"to" : "2026-07-17T23:59:59",
    "sortBy": "publishedAt"
}
    response = requests.get(url_api, params=params)
    
    if response.status_code == 200:
        articles = response.json()['articles']
        #print(response.json()["totalResults"])
        #print(response.json())
        #print(response.url)
        return articles
        
    
    else:
        raise ConnectionError("No se pudieron obtener las noticias.")
    
    
zona_local = ZoneInfo("America/Argentina/Buenos_Aires")
hasta = datetime.now(zona_local)
"""desde = hasta.replace(
    hour = 0,
    minute = 0,
    second = 0,
    microsecond = 0
)"""
desde = hasta - timedelta(hours=48)
#desde = datetime(2026, 7, 16, 0, 0, 0)
#hasta = datetime(2026, 7, 16, 23, 59, 59)

noticias = obtener_noticias("World Cup", desde, hasta)
#print(desde)
#print(hasta)

#Fin obtener_noticias()



#Empieza guardar_noticias()
def guardar_noticias(lista_noticias):
    
    fetched_at = datetime.now(zona_local).isoformat()

    conn = sqlite3.connect("database/db.db")   
    cursor = conn.cursor() 

    urls_guardadas = []

    for article in lista_noticias:
        title = article['title']
        source = article['source']['name']
        description = article['description']
        published_at = article['publishedAt']
        url_article = article['url']
        #print(json.dumps(article, indent=4))     
        
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
        
                   
        if cursor.rowcount == 1:        #es un atributo del cursor que indica cuántas filas fueron afectadas por la última sentencia SQL que ejecutaste con ese cursor.
            urls_guardadas.append(url_article)
        

    conn.commit()   
    conn.close()            
    
    return urls_guardadas  

urls_guardadas = guardar_noticias(noticias)
#Fin guardar_noticias()


#Empieza preparar_correo()
def preparar_correo(lista_urls):
    if len(lista_urls) >= 1:
    
        msg = EmailMessage()
        
        msg['From'] = GMAIL_USER
        msg['To'] = GMAIL_USER
        msg['Subject'] = 'Noticias de hoy'
        cuerpo_mail = '\n'.join(lista_urls)
        msg.set_content(cuerpo_mail)
        return msg

msg = preparar_correo(urls_guardadas)
#Fin preparar_correo()



#Empieza enviar_correo()
def enviar_correo(mensaje):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(GMAIL_USER, GMAIL_PASSWORD)
    server.send_message(mensaje)
    server.quit()
    
enviar_correo(msg)
#Fin enviar_correo()





