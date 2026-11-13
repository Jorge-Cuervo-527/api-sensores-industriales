# 🏗️ Arquitectura del Sistema y Decisiones de Diseño

Este documento expone la arquitectura técnica de la **API de Sensores Industriales**, justificando las decisiones de diseño adoptadas y detallando los flujos de ejecución tanto para peticiones válidas como para casos de error.

---

## 🏛️ Diagrama de Arquitectura en Capas

El flujo de información sigue un modelo desacoplado y unidireccional:

```text
+-------------------------------------------------------------+
|                     CLIENTE HTTP                            |
|        (Navegador / Swagger / curl / Postman / tests)       |
+-------------------------------------------------------------+
                              │  HTTP Request (JSON)
                              ▼
+-------------------------------------------------------------+
|                      CAPA WEB (FastAPI)                     |
|           • Ruteo y controladores HTTP                      |
|           • Manejo centralizado de excepciones (errors.py)  |
|           • Serialización de respuestas (serialize)         |
+-------------------------------------------------------------+
                              │  Validación y parsing
                              ▼
+-------------------------------------------------------------+
|                   CAPA DE DOMINIO (Pydantic v2)             |
|           • Esquemas SensorBase, SensorCreate, SensorUpdate |
|           • Validadores @field_validator y rangos físicos   |
|           • Conversión tipada de tipos primitivos a objetos |
+-------------------------------------------------------------+
                              │  Documento validado (dict)
                              ▼
+-------------------------------------------------------------+
|                 CAPA DE PERSISTENCIA (PyMongo)              |
|           • Cliente singleton MongoClient                   |
|           • Conexión por pooling síncrono                   |
|           • Operaciones CRUD sobre colección 'sensores'     |
+-------------------------------------------------------------+
                              │  Protocolo de cable MongoDB
                              ▼
+-------------------------------------------------------------+
|                   MOTOR NoSQL (MongoDB)                     |
|           • Base de datos: 'monitoreo_industrial'           |
|           • Colección: 'sensores' (BSON con _id ObjectId)   |
+-------------------------------------------------------------+
```

---

## ⚖️ Justificación de Decisiones de Diseño

### 1. ¿Por qué FastAPI y no Flask?
* **Validación Nativa:** FastAPI integra Pydantic de manera nativa en el ciclo de vida de la petición, evitando escribir código manual de parseo y validación de tipos.
* **Documentación Automática OpenAPI:** Genera automáticamente la documentación interactiva en Swagger UI (`/docs`) y ReDoc (`/redoc`) sin librerías adicionales.
* **Rendimiento:** Está basado en el estándar ASGI (Starlette) con un alto desempeño en el manejo de solicitudes concurrentes.
* **Tipado Estricto:** Obliga al uso de Type Hints modernos de Python (PEP 484), mejorando la legibilidad y reduciendo drásticamente errores en tiempo de ejecución.

### 2. ¿Por qué PyMongo síncrono y no Motor (async)?
* **Adecuación al Ámbito Académico:** PyMongo es la biblioteca canónica oficial mantenida por MongoDB Inc. Su modelo síncrono e imperativo es el más claro para el entendimiento conceptual de operaciones CRUD NoSQL.
* **Simplicidad y Menor Sobrecarga:** Evita la complejidad de gestionar eventos de bucle asíncrono (`asyncio`), `await` en llamadas de base de datos y deadlocks en hilos de prueba.
* **Suficiencia de Carga:** Para el volumen de datos de este proyecto (monitoreo de sensores industriales en laboratorio), el pooling nativo de conexiones síncronas de PyMongo es extraordinariamente eficiente.

### 3. ¿Por qué Pydantic v2?
* **Motor en Rust (`pydantic-core`):** Pydantic v2 fue completamente reescrito con un núcleo en Rust, ofreciendo una velocidad de validación hasta 15 veces más rápida que v1.
* **Validadores Modernos:** Utiliza decoradores estandarizados como `@field_validator` con acceso contextual a otros campos a través de `ValidationInfo`, lo que permite validar el `valor` contra el `tipo` de sensor de forma limpia.
* **Compatibilidad con FastAPI 0.115+:** Es el estándar moderno requerido para las últimas versiones de FastAPI.

### 4. ¿Por qué separar `models.py` de `main.py`?
* **Principio de Responsabilidad Única (SRP):** `models.py` contiene exclusivamente la lógica y reglas de dominio (qué es un sensor y qué valores puede tomar), mientras que `main.py` se encarga del ruteo HTTP y la interacción con el cliente.
* **Reutilización y Mantenibilidad:** Permite importar los modelos en scripts independientes (como `seed_data.py` o los tests) sin necesidad de cargar toda la aplicación web de FastAPI.

---

## 🔄 Flujo de una Petición Exitosa (`POST /sensores/`)

```text
Cliente               FastAPI               Pydantic              PyMongo              MongoDB
   │                     │                     │                     │                    │
   │─── POST JSON ──────>│                     │                     │                    │
   │                     │── Parsear cuerpo ──>│                     │                    │
   │                     │                     │── Validar rango ───┐│                    │
   │                     │                     │<── Rango OK ───────┘│                    │
   │                     │<── SensorCreate ────│                     │                    │
   │                     │                                           │                    │
   │                     │── insert_one(doc) ───────────────────────>│                    │
   │                     │                                           │── Protocol BSON ──>│
   │                     │                                           │<── InsertedId ─────│
   │                     │<── Resultado inserción ───────────────────│                    │
   │                     │                                           │                    │
   │                     │── serialize(_id -> id)                    │                    │
   │<── 201 Created ─────│                                           │                    │
```

---

## 🛑 Flujo de una Petición con Error de Validación (`HTTP 422`)

Si el cliente envía un dato inválido (por ejemplo: `tipo="humedad"` o `presion` con `valor=999`):

```text
Cliente               FastAPI               Pydantic           (MongoDB NO ES CONSULTADO)
   │                     │                     │
   │─── POST JSON ──────>│                     │
   │                     │── Parsear cuerpo ──>│
   │                     │                     │── Validar tipo / rango
   │                     │                     │   ❌ ERROR: 999 fuera de [0, 500]
   │                     │<── ValidationError ─│
   │                     │
   │                     │── manejador_validacion_error() (errors.py)
   │<── 422 Unprocessable│
   │    Entity (JSON)    │
```

> 🛡️ **Garantía de Integridad:** La petición **se detiene en la Capa de Dominio** y nunca llega a la base de datos, protegiendo a MongoDB de inconsistencias o datos corruptos.
