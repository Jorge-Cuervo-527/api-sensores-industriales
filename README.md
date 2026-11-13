# 🏭 API RESTful para Monitoreo de Sensores Industriales (EA2)

Bienvenido al repositorio del proyecto **EA2: Bases de datos NoSQL y operaciones CRUD**.

Este proyecto implementa una API RESTful desarrollada con **FastAPI** y **MongoDB** para la ingesta, validación y consulta de lecturas de sensores industriales (`temperatura`, `presion` y `vibracion`).

---

## 📖 Documentación Completa

Toda la documentación técnica, guías de instalación, uso y especificaciones se encuentran organizadas en la carpeta [`docs/`](docs/):

1. 📘 [**docs/README.md**](docs/README.md) — Índice general, resumen ejecutivo, badges y quickstart.
2. ⚙️ [**docs/INSTALACION.md**](docs/INSTALACION.md) — Guía de instalación paso a paso (Windows, macOS, Linux y Atlas).
3. 🚀 [**docs/USO.md**](docs/USO.md) — Cómo iniciar el servidor, sembrar datos y explorar Swagger / ReDoc.
4. 📡 [**docs/ENDPOINTS.md**](docs/ENDPOINTS.md) — Especificación detallada de los 4 endpoints CRUD, códigos HTTP y ejemplos.
5. 🧪 [**docs/PRUEBAS.md**](docs/PRUEBAS.md) — Guía de pruebas automatizadas (`pytest`), manuales (`curl`) y Postman.
6. 🏗️ [**docs/ARQUITECTURA.md**](docs/ARQUITECTURA.md) — Diagramas de flujo, diseño en capas y justificación de decisiones.
7. 🔧 [**docs/TROUBLESHOOTING.md**](docs/TROUBLESHOOTING.md) — Solución a los 8 errores más frecuentes.

---

## ⚡ Quickstart Rápido

```bash
# 1. Crear y activar entorno virtual
python -m venv venv
# En Windows: .\venv\Scripts\activate | En Linux/macOS: source venv/bin/activate

# 2. Instalar dependencias exactas
pip install -r requirements.txt

# 3. Poblar la base de datos con datos semilla
python scripts/seed_data.py

# 4. Iniciar la API
uvicorn app.main:app --reload

# 5. Ejecutar suite de pruebas
pytest tests/ -v
```

Acceso a la interfaz interactiva: [http://localhost:8000/docs](http://localhost:8000/docs)
