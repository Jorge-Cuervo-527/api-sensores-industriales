# 🧪 Manual de Pruebas: Automatizadas, Manuales y Validación

Este documento detalla todas las estrategias de prueba diseñadas y ejecutadas para garantizar el correcto funcionamiento de la API, cubriendo pruebas automatizadas con **pytest**, pruebas mediante línea de comandos con **curl / PowerShell** y pruebas mediante **Postman**.

---

## 🤖 1. Pruebas Automáticas con Pytest

La suite de pruebas automatizadas está ubicada en `tests/test_api.py` y utiliza `pytest` junto con el cliente `TestClient` de FastAPI / Starlette (basado en `httpx`).

### Comando de Ejecución
```bash
pytest tests/ -v
```

### Detalle de los 9 Tests Implementados

| # | Nombre de la Prueba | Propósito | Resultado Esperado |
|---|---|---|:---:|
| 1 | `test_crear_sensor_valido` | Envía un payload válido de temperatura | `HTTP 201 Created` con `id` asignado |
| 2 | `test_crear_sensor_tipo_invalido` | Intenta registrar un sensor con `tipo="humedad"` | `HTTP 422 Unprocessable Entity` |
| 3 | `test_crear_sensor_fuera_de_rango` | Intenta registrar presión con `valor=999.0` (máx. 500) | `HTTP 422 Unprocessable Entity` |
| 4 | `test_listar_sensores` | Inserta 2 sensores y consulta el listado global | `HTTP 200 OK` con lista de longitud 2 |
| 5 | `test_filtrar_por_tipo` | Consulta con query param `?tipo=temperatura` | `HTTP 200 OK` retornando solo dicho tipo |
| 6 | `test_actualizar_sensor_existente` | Actualiza valor y ubicación del sensor de temperatura | `HTTP 200 OK` con datos actualizados |
| 7 | `test_actualizar_sensor_inexistente` | Intenta hacer PUT sobre un tipo no existente | `HTTP 404 Not Found` |
| 8 | `test_eliminar_sensor_existente` | Elimina el primer sensor de vibración | `HTTP 204 No Content` sin cuerpo |
| 9 | `test_eliminar_sensor_inexistente` | Intenta hacer DELETE sobre un tipo que no existe | `HTTP 404 Not Found` |

---

## 💻 2. Pruebas Manuales con Script Bash (`curl`)

El script automatizado `scripts/pruebas_curl.sh` ejecuta la secuencia completa de operaciones CRUD:

```bash
bash scripts/pruebas_curl.sh
```

*(En Windows también dispone de la versión nativa `powershell -ExecutionPolicy Bypass -File scripts/pruebas_curl.ps1`).*

### Secuencia del Flujo:
1. **POST:** Crea un sensor de temperatura inicial (`HTTP 201`).
2. **GET:** Recupera todos los sensores de la colección (`HTTP 200`).
3. **GET filtrado:** Consulta únicamente sensores de tipo temperatura (`HTTP 200`).
4. **PUT:** Modifica la lectura y ubicación del sensor (`HTTP 200`).
5. **GET de comprobación:** Verifica que los cambios persistan en MongoDB (`HTTP 200`).
6. **DELETE:** Elimina el registro de temperatura creado (`HTTP 204`).
7. **GET final:** Valida que el sensor ya no figure en la base de datos (`HTTP 200`).

---

## 📮 3. Pruebas Manuales con Postman (Paso a Paso)

Para presentar evidencias o capturas de pantalla de la evaluación académica:

### Paso 1: Crear la Colección
1. Abra Postman y haga clic en **New -> Collection**.
2. Nombre la colección: `EA2 - Monitoreo Sensores`.
3. Defina una variable de colección llamada `baseUrl` con el valor `http://localhost:8000`.

### Paso 2: Configurar las 5 Solicitudes Principales
1. **Crear Sensor (POST):**
   * URL: `{{baseUrl}}/sensores/`
   * Método: `POST`
   * Headers: `Content-Type: application/json`
   * Body (raw JSON):
     ```json
     {
       "tipo": "presion",
       "valor": 120.5,
       "ubicacion": "Compresor Secundario",
       "fecha": "2026-11-11T10:00:00"
     }
     ```
   * *Captura a tomar:* Código `201 Created` y el JSON devuelto con su `id`.

2. **Listar Todos (GET):**
   * URL: `{{baseUrl}}/sensores/`
   * Método: `GET`
   * *Captura a tomar:* Código `200 OK` y el array con los sensores.

3. **Filtrar por Tipo (GET):**
   * URL: `{{baseUrl}}/sensores/?tipo=presion`
   * Método: `GET`
   * *Captura a tomar:* Código `200 OK` con solo sensores de presión.

4. **Actualizar Sensor (PUT):**
   * URL: `{{baseUrl}}/sensores/presion`
   * Método: `PUT`
   * Body (raw JSON):
     ```json
     {
       "valor": 185.0,
       "ubicacion": "Compresor Secundario - Ajustado"
     }
     ```
   * *Captura a tomar:* Código `200 OK` y el nuevo valor reflejado.

5. **Eliminar Sensor (DELETE):**
   * URL: `{{baseUrl}}/sensores/presion`
   * Método: `DELETE`
   * *Captura a tomar:* Código `204 No Content` con respuesta vacía.

---

## ⚠️ 4. Pruebas de Casos de Error (Casos Borde)

Para verificar la robustez de las validaciones de negocio:

### Caso A: Tipo de Sensor Inválido (HTTP 422)
* **Petición:** `POST http://localhost:8000/sensores/`
* **Body:**
  ```json
  {
    "tipo": "humedad",
    "valor": 50.0,
    "ubicacion": "Silo 4",
    "fecha": "2026-11-11T10:00:00"
  }
  ```
* **Respuesta esperada:** `HTTP 422 Unprocessable Entity` indicando que `tipo` solo acepta `temperatura`, `presion` o `vibracion`.

### Caso B: Valor Fuera de Rango (HTTP 422)
* **Petición:** `POST http://localhost:8000/sensores/`
* **Body:**
  ```json
  {
    "tipo": "vibracion",
    "valor": 12.8,
    "ubicacion": "Turbina Principal",
    "fecha": "2026-11-11T10:00:00"
  }
  ```
* **Respuesta esperada:** `HTTP 422 Unprocessable Entity` con mensaje: *"El valor para 'vibracion' debe estar entre 0.0 y 5.0."*

### Caso C: Eliminación de Tipo Inexistente (HTTP 404)
* **Petición:** `DELETE http://localhost:8000/sensores/desconocido`
* **Respuesta esperada:** `HTTP 404 Not Found` con mensaje: *"No se encontró ningún sensor de tipo 'desconocido' para eliminar."*
