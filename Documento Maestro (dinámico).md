# Estado del Proyecto

## Estado actual

### Completado

- [x] Conexión con NewsAPI
- [x] Descarga de noticias
- [x] Manejo de errores HTTP
- [x] Comprensión del JSON
- [x] Creación de SQLite
- [x] Diseño de raw_news

---

### En desarrollo

- [ ] Recorrer articles
- [ ] Extraer campos
- [ ] Insertar noticias

---

### Próximo objetivo

Implementar el recorrido de `articles` y analizar cuidadosamente cómo construir la inserción en SQLite.

---

## Decisiones tomadas

### Fecha de descarga

- Se calcula una única vez antes del `for`.
- Representa la fecha de descarga del lote.
- Se almacena en formato ISO.

### Base de datos

- SQLite.
- Acceso mediante `sqlite3`.
- Sin ORM.

---

## Conceptos aprendidos

- requests
- response.json()
- estructura de articles
- datetime
- SQLite básico

---

## Bitácora

### 2026-06-17

- Se decidió registrar una única fecha para todo el lote descargado.

### 2026-06-20

- Se decidió no utilizar pandas.

### 2026-07-02

- Se creó la documentación del proyecto.

---

## Backlog

### Alta prioridad

- Recorrer articles
- Inserción en SQLite
- Logging

### Media prioridad

- Variables de entorno
- Configuración
- Docker

### Baja prioridad

- Cloud
- CI/CD