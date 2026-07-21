# Troubleshooting Log

## Proyecto: World Cup 2026 News Pipeline

---

# Problema: NewsAPI no devuelve resultados con ventana temporal dinámica

## Contexto

Durante las pruebas del pipeline se observó que la extracción de noticias funcionaba correctamente utilizando fechas definidas manualmente, pero no devolvía resultados cuando la ventana temporal era generada dinámicamente mediante Python.

La intención inicial era obtener todas las noticias publicadas durante el día actual.

La lógica utilizada era:

```python
hasta = datetime.now(zona_local)

desde = hasta.replace(
    hour=0,
    minute=0,
    second=0,
    microsecond=0
)
```

---

## Síntoma observado

La API respondía correctamente:

```json
{
    "status": "ok",
    "totalResults": 0,
    "articles": []
}
```

Esto indicaba que:

- la conexión con NewsAPI funcionaba;
- las credenciales eran correctas;
- la petición HTTP era válida;

pero no existían artículos dentro del intervalo solicitado.

---

## Investigación

Se compararon los parámetros enviados a la API.

### Ventana temporal fija

Ejemplo:

```text
from=2026-07-16T00:00:00
to=2026-07-17T23:59:59
```

La API devolvía noticias correctamente.

---

### Ventana temporal dinámica

Ejemplo:

```text
from=2026-07-17T00:00:00-03:00
to=2026-07-17T11:32:07-03:00
```

La respuesta era diferente.

Se observó que los timestamps generados dinámicamente incluían información de zona horaria.

Además, se identificó que las fuentes internacionales pueden publicar noticias utilizando diferentes referencias horarias, por lo que una ventana estricta basada en el día local podía excluir publicaciones relevantes.

---

## Decisión tomada

Se decidió utilizar una ventana temporal móvil:

```python
desde = hasta - timedelta(hours=48)
```

Esto permite:

- reducir la dependencia del huso horario de cada fuente;
- evitar perder noticias publicadas cerca del cambio de día;
- asegurar una cantidad suficiente de noticias para el reporte diario.

---

## Aprendizaje

Las APIs externas pueden tener comportamientos sensibles a:

- formatos de fecha;
- zonas horarias;
- ventanas temporales demasiado restrictivas.

Antes de asumir que un problema pertenece al código, es necesario inspeccionar la petición real enviada al servicio externo.

---

# Problema: ejecución correcta del pipeline pero ausencia de correo electrónico

## Contexto

Durante algunas ejecuciones el pipeline finalizaba sin errores visibles, pero no se recibía ningún correo electrónico.

Inicialmente esto podía interpretarse como un fallo del envío.

---

## Investigación

Se analizó el flujo completo:

```text
Obtención de noticias
        ↓
Inserción en SQLite
        ↓
Detección de noticias nuevas
        ↓
Preparación del correo
        ↓
Envío mediante SMTP
```

Se verificó que:

- la API podía devolver noticias correctamente;
- SQLite almacenaba los datos;
- la restricción:

```sql
url TEXT UNIQUE
```

evitaba duplicados;
- `INSERT OR IGNORE` descartaba automáticamente noticias ya existentes.

---

## Análisis del comportamiento

La lista utilizada para decidir si enviar correo era:

```python
urls_guardadas = []
```

Si todas las noticias obtenidas desde la API ya estaban almacenadas, no se insertaban nuevos registros y la lista permanecía vacía.

Esto no representaba un error.

Era un estado válido del pipeline:

```text
Pipeline ejecutado correctamente

        ↓

No hay noticias nuevas

        ↓

No se envía correo
```

---

## Aprendizaje

Se identificó la importancia de diferenciar tres escenarios:

### 1. Pipeline fallido

Ejemplo:

- error de conexión;
- credenciales inválidas;
- error de base de datos.

---

### 2. Pipeline exitoso sin nuevos datos

Ejemplo:

- todas las noticias obtenidas ya estaban almacenadas.

---

### 3. Pipeline exitoso con nuevos datos

Ejemplo:

- nuevas noticias insertadas;
- correo generado y enviado.

---

## Mejora futura

Incorporar logging estructurado para registrar:

- fecha y hora de ejecución;
- cantidad de noticias obtenidas desde la API;
- cantidad de noticias nuevas insertadas;
- estado del envío del correo.

Esto permitirá distinguir automáticamente entre errores y ejecuciones exitosas sin nuevos datos.

---

# Problema: organización inicial del script

## Contexto

La primera versión del pipeline funcionaba correctamente, pero todo el flujo estaba escrito de forma secuencial dentro del archivo principal.

Esto dificultaba:

- leer el flujo general;
- reutilizar funciones;
- realizar pruebas individuales.

---

## Solución aplicada

Se realizó una refactorización separando responsabilidades:

```text
obtener_noticias()

        ↓

guardar_noticias()

        ↓

preparar_correo()

        ↓

enviar_correo()
```

Además se incorporó una función principal:

```python
def main():
```

encargada de coordinar el flujo.

---

## Aprendizaje

La modularización permite que cada componente tenga una responsabilidad clara y facilita futuras mejoras como:

- pruebas automatizadas;
- manejo de excepciones;
- incorporación de nuevos pasos al pipeline.

---

# Mejoras futuras relacionadas con troubleshooting

A partir de estos problemas surgieron las siguientes mejoras previstas:

- Incorporar logging estructurado.
- Registrar métricas básicas del pipeline.
- Mejorar manejo de excepciones.
- Agregar validaciones de datos antes de insertar en SQLite.
- Incorporar pruebas automatizadas.