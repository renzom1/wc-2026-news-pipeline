import requests
import json
import sqlite3      #importamos sqlite3 desde Python (no es un paquete)
from datetime import datetime, UTC
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
    "sortBy": "publishedAt"
}
    response = requests.get(url_api, params=params)
    
    if response.status_code == 200:
        articles = response.json()['articles']
        return articles
        
    
    else:
        raise ConnectionError("No se pudieron obtener las noticias.")
    
    
zona_local = ZoneInfo("America/Argentina/Buenos_Aires")
hasta = datetime.now(zona_local)
desde = hasta.replace(
    hour = 0,
    minute = 0,
    second = 0,
    microsecond = 0
)
noticias = obtener_noticias("Argentina", desde, hasta)









#Empieza guardar_noticias()
fetched_at = datetime.now(zona_local).isoformat()

conn = sqlite3.connect("database/db.db")   
cursor = conn.cursor() 

#total_articles = len(articles)
#processed =
inserted = 0 
ignored = 0 
urls_enviadas = []

for article in noticias:
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
    
    
    cursor.rowcount                     #es un atributo del cursor que indica cuántas filas fueron afectadas por la última sentencia SQL que ejecutaste con ese cursor.
    if cursor.rowcount == 1:
        inserted += 1
        urls_enviadas.append(url_article)
        
    else:
        ignored += 1
    
    #print(url_article)
    #print(published_at)
    #print(title)
    



conn.commit()   
conn.close()              
#Fin guardar_noticias()
#print("Insertadas:", inserted)
#print("Ignoradas:", ignored)
#print("URLs enviadas:", urls_enviadas)

#print(total_articles)
#print(inserted)
#print(ignored)
#print(urls_enviadas)
#print(len(urls_enviadas))        
#print('\n'.join(urls_enviadas))

#Empieza preparar_correo()
if len(urls_enviadas) >= 1:
    
    msg = EmailMessage()
    
    msg['From'] = GMAIL_USER
    msg['To'] = GMAIL_USER
    msg['Subject'] = 'Noticias de hoy'
    cuerpo_mail = '\n'.join(urls_enviadas)
    msg.set_content(cuerpo_mail)
#Fin preparar_correo()

    #Empieza enviar_correo()
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(GMAIL_USER, GMAIL_PASSWORD)
    #print(GMAIL_USER)
    #print(GMAIL_PASSWORD)
    #print('Envío el correo')
    server.send_message(msg)
    server.quit()
    #Fin enviar_correo()





