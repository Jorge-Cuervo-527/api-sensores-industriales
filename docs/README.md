# 🏭 API RESTful para Monitoreo de Sensores Industriales

> API RESTful robusta y tipada construida con FastAPI y MongoDB para la gestión y validación de variables de planta industrial.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?logo=fastapi)
![MongoDB](https://img.shields.io/badge/MongoDB-Community%20%7C%20Atlas-47A248?logo=mongodb)
![Pydantic](https://img.shields.io/badge/Pydantic-v2.9.2-E92063?logo=pydantic)
![Pytest](https://img.shields.io/badge/Tests-Pytest%20(9%2F9%20Pass)-brightgreen?logo=pytest)
![Licencia](https://img.shields.io/badge/Licencia-Académica%20EA2-orange)

---

## 📑 Tabla de Contenidos

| Documento | Descripción |
|---|---|
| [**INSTALACION.md**](INSTALACION.md) | Guía exhaustiva de instalación por sistema operativo y configuración de base de datos. |
| [**USO.md**](USO.md) | Manual operativo: arranque del servicio, endpoints de documentación interactiva y parada limpia. |
| [**ENDPOINTS.md**](ENDPOINTS.md) | Catálogo de rutas, métodos, payloads de entrada/salida y códigos de estado HTTP. |
| [**PRUEBAS.md**](PRUEBAS.md) | Ejecución de pruebas unitarias/integración con `pytest`, scripts `curl` y colección de Postman. |
| [**ARQUITECTURA.md**](ARQUITECTURA.md) | Diagramas conceptuales de arquitectura, flujos de validación y justificación técnica de tecnologías. |
| [**TROUBLESHOOTING.md**](TROUBLESHOOTING.md) | Matriz de diagnóstico y resolución de errores comunes en desarrollo y despliegue. |

---

## ⚡ Quickstart (Arranque en 5 comandos)

```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno virtual (Windows)
.\venv\Scripts\activate

# 3. Instalar dependencias requeridas
pip install -r requirements.txt

# 4. Sembrar datos de ejemplo (3 sensores industriales)
python scripts/seed_data.py

# 5. Iniciar la API con recarga automática
uvicorn app.main:app --reload
```

* Swagger UI interactivo: [http://localhost:8000/docs](http://localhost:8000/docs)
* Documentación ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📁 Estructura del Proyecto

```
ea2_api_sensores/
├── app/
│   ├── __init__.py          # Inicializador de paquete
│   ├── main.py              # Aplicación FastAPI, rutas y serialización
│   ├── database.py          # Conexión persistente y gestión de cliente PyMongo
│   ├── models.py            # Modelos y esquemas Pydantic v2 con validación
│   └── errors.py            # Manejo centralizado de excepciones y respuestas HTTP
├── tests/
│   ├── __init__.py          # Inicializador de paquete de pruebas
│   └── test_api.py          # 9 pruebas automatizadas con pytest y TestClient
├── scripts/
│   ├── pruebas_curl.sh      # Secuencia bash automatizada de pruebas CRUD
│   ├── pruebas_curl.ps1     # Secuencia PowerShell automatizada para Windows
│   └── seed_data.py         # Inserción inicial de 3 sensores de referencia
├── docs/
│   ├── README.md            # Entrada principal de la documentación técnica
│   ├── INSTALACION.md       # Procedimientos de instalación multiplataforma
│   ├── USO.md               # Instrucciones de ejecución y operación
│   ├── ENDPOINTS.md         # Documentación formal de contratos de API
│   ├── PRUEBAS.md           # Metodología y reporte de pruebas
│   ├── ARQUITECTURA.md      # Justificaciones de diseño y diagramas ASCII
│   └── TROUBLESHOOTING.md   # Resolución de incidentes y fallos frecuentes
├── requirements.txt         # Dependencias con versiones fijadas
├── .gitignore               # Reglas de exclusión para Git
└── README.md                # Entrada raíz del repositorio
```

---

## 🧰 Stack Tecnológico

* **Lenguaje:** Python 3.11 (compatible con 3.10+)
* **Framework Web:** FastAPI `0.115.0`
* **Servidor ASGI:** Uvicorn `0.32.0`
* **Base de Datos NoSQL:** MongoDB Community / MongoDB Atlas
* **Driver de Base de Datos:** PyMongo `4.10.1` (síncrono)
* **Validación de Datos:** Pydantic `2.9.2`
* **Testing:** Pytest `8.3.3` + HTTPX `0.27.2`

---

## 👨‍💻 Autor y Metadatos

* **Autor:** Jorge Eliecer Cuervo
* **Actividad:** EA2 — Bases de datos NoSQL y operaciones CRUD
* **materia:** Tecnologías Web
* **Programa:** Tecnología en desarrollo de software
* **Fecha:** Noviembre 2026
* **Estado:** Completado y validado (100% pruebas aprobadas)
