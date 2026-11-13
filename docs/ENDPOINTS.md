# 📡 Especificación y Referencia de Endpoints

Este documento detalla los 4 endpoints implementados en la API para la gestión del ciclo de vida de los sensores industriales (**CRUD**).

---

## 📋 Tabla Resumen de Endpoints

| Método | Ruta | Descripción | Código Éxito | Códigos de Error |
|:---|:---|:---|:---:|:---:|
| `POST` | `/sensores/` | Registra una nueva lectura de sensor en la base de datos | `201 Created` | `422`, `500` |
| `GET` | `/sensores/` | Lista todas las lecturas de sensores registradas | `200 OK` | `500` |
| `GET` | `/sensores/?tipo={tipo}` | Filtra las lecturas por tipo (`temperatura`, `presion`, `vibracion`) | `200 OK` | `500` |
| `PUT` | `/sensores/{tipo}` | Actualiza el primer sensor encontrado del tipo indicado | `200 OK` | `404`, `422`, `500` |
| `DELETE` | `/sensores/{tipo}` | Elimina el primer sensor encontrado del tipo indicado | `204 No Content` | `404`, `500` |

---

## 📐 Rangos de Operación Válidos por Tipo de Sensor

| Tipo de Sensor | Valor Mínimo | Valor Máximo | Unidad de Medida |
|---|:---:|:---:|:---:|
| `temperatura` | -10.0 | 100.0 | °C (Grados Celsius) |
| `presion` | 0.0 | 500.0 | kPa (Kilopascales) |
| `vibracion` | 0.0 | 5.0 | mm/s (Milímetros por segundo) |

---

## 1. Crear Sensor (`POST /sensores/`)

Crea un nuevo documento de sensor previa validación de tipo y rango admitido.

* **Método:** `POST`
* **Ruta:** `/sensores/`
* **Content-Type:** `application/json`

### Request Body de Ejemplo
```json
{
  "tipo": "temperatura",
  "valor": 28.5,
  "ubicacion": "Caldera Principal - Sector Norte",
  "fecha": "2026-11-11T08:45:00"
}
```

### Response de Ejemplo (`201 Created`)
```json
{
  "id": "6af46dd87b8eca15695d3bce",
  "tipo": "temperatura",
  "valor": 28.5,
  "ubicacion": "Caldera Principal - Sector Norte",
  "fecha": "2026-11-11T08:45:00"
}
```

### Posibles Códigos de Error
* **`422 Unprocessable Entity`:**
  * Si `tipo` no es uno de: `temperatura`, `presion`, `vibracion`.
  * Si `valor` excede el rango permitido para ese tipo (ej. `temperatura` a 150 °C).
  * Si `ubicacion` está vacía o supera los 100 caracteres.
  * Si `fecha` no respeta el formato ISO 8601.
* **`500 Internal Server Error`:** Si ocurre una falla en el servidor o motor de base de datos.

### Ejemplo con `curl`
```bash
curl -X POST "http://localhost:8000/sensores/" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "temperatura",
    "valor": 28.5,
    "ubicacion": "Caldera Principal - Sector Norte",
    "fecha": "2026-11-11T08:45:00"
  }'
```

---

## 2. Listar Sensores (`GET /sensores/`)

Obtiene la colección de sensores. Puede consultar todos los registros o filtrar mediante el query parameter opcional `tipo`.

* **Método:** `GET`
* **Ruta:** `/sensores/`
* **Parámetros Query:**
  * `tipo` *(opcional, string)*: Filtra por `temperatura`, `presion` o `vibracion`.

### Response de Ejemplo (`200 OK`)
```json
[
  {
    "id": "6af46dd87b8eca15695d3bce",
    "tipo": "temperatura",
    "valor": 23.8,
    "ubicacion": "Horno de Secado - Nave A",
    "fecha": "2026-11-11T08:00:00Z"
  },
  {
    "id": "6af46dd87b8eca15695d3bcf",
    "tipo": "presion",
    "valor": 175.5,
    "ubicacion": "Compresor Principal - Sala de Máquinas",
    "fecha": "2026-11-11T08:15:00Z"
  }
]
```

### Posibles Códigos de Error
* **`500 Internal Server Error`:** Falla de conexión a MongoDB.

### Ejemplos con `curl`
```bash
# Consultar todos los sensores
curl -X GET "http://localhost:8000/sensores/"

# Filtrar únicamente por sensores de presión
curl -X GET "http://localhost:8000/sensores/?tipo=presion"
```

---

## 3. Actualizar Sensor por Tipo (`PUT /sensores/{tipo}`)

Actualiza el primer registro que coincida con el `tipo` especificado en la ruta. Admite actualización parcial o total de los campos `valor`, `ubicacion` y `fecha`.

* **Método:** `PUT`
* **Ruta:** `/sensores/{tipo}`
* **Parámetros de Ruta:**
  * `tipo` *(obligatorio, string)*: `temperatura`, `presion` o `vibracion`.
* **Content-Type:** `application/json`

### Request Body de Ejemplo
```json
{
  "valor": 45.0,
  "ubicacion": "Horno de Secado - Nave A (Mantenimiento Realizado)",
  "fecha": "2026-11-11T09:15:00"
}
```

### Response de Ejemplo (`200 OK`)
```json
{
  "id": "6af46dd87b8eca15695d3bce",
  "tipo": "temperatura",
  "valor": 45.0,
  "ubicacion": "Horno de Secado - Nave A (Mantenimiento Realizado)",
  "fecha": "2026-11-11T09:15:00"
}
```

### Posibles Códigos de Error
* **`404 Not Found`:** Si no existe ningún sensor del tipo indicado en la base de datos.
* **`422 Unprocessable Entity`:** Si el nuevo `valor` se encuentra fuera del rango admitido para ese `tipo`.
* **`500 Internal Server Error`:** Error inesperado en base de datos.

### Ejemplo con `curl`
```bash
curl -X PUT "http://localhost:8000/sensores/temperatura" \
  -H "Content-Type: application/json" \
  -d '{
    "valor": 45.0,
    "ubicacion": "Horno de Secado - Nave A (Mantenimiento Realizado)",
    "fecha": "2026-11-11T09:15:00"
  }'
```

---

## 4. Eliminar Sensor por Tipo (`DELETE /sensores/{tipo}`)

Elimina el primer sensor encontrado que coincida con el `tipo` indicado en la ruta.

* **Método:** `DELETE`
* **Ruta:** `/sensores/{tipo}`
* **Parámetros de Ruta:**
  * `tipo` *(obligatorio, string)*: Tipo de sensor a eliminar.

### Response de Ejemplo (`204 No Content`)
* **Código HTTP:** `204 No Content`
* **Cuerpo de Respuesta:** Vacío (sin contenido).

### Posibles Códigos de Error
* **`404 Not Found`:** Si no existe ningún sensor del tipo solicitado.
  ```json
  {
    "detalle": "No se encontró ningún sensor de tipo 'inexistente' para eliminar."
  }
  ```
* **`500 Internal Server Error`:** Falla interna de la base de datos.

### Ejemplo con `curl`
```bash
curl -i -X DELETE "http://localhost:8000/sensores/temperatura"
```
*(El flag `-i` muestra las cabeceras HTTP, verificando el código `HTTP/1.1 204 No Content`).*
