# 🚀 Guía de Uso y Operación de la API

Esta guía contiene las instrucciones necesarias para iniciar, operar, consultar y detener la **API de Monitoreo de Sensores Industriales**.

---

## 🏁 1. Precarga de Datos de Ejemplo (Seed)

Antes de levantar el servidor por primera vez, o para restablecer la base de datos a un estado conocido con 3 sensores de prueba (uno de cada tipo admitido), ejecute:

```bash
python scripts/seed_data.py
```

Salida esperada en consola:
```text
============================================================
🌱 INICIANDO CARGA DE DATOS DE EJEMPLO (SEED)...
============================================================
🧹 Registros anteriores eliminados: 0
✅ Se insertaron exitosamente 3 sensores:
  • [TEMPERATURA] - ID: 6af46dd87b8eca...
    Valor: 23.8 | Ubicación: Horno de Secado - Nave A
    Fecha: 2026-11-11T08:00:00+00:00

  • [PRESION] - ID: 6af46dd87b8eca...
    Valor: 175.5 | Ubicación: Compresor Principal - Sala de Máquinas
    Fecha: 2026-11-11T08:15:00+00:00

  • [VIBRACION] - ID: 6af46dd87b8eca...
    Valor: 1.45 | Ubicación: Bomba Centrífuga B-101 - Sector Oeste
    Fecha: 2026-11-11T08:30:00+00:00

✨ Carga de datos completada con éxito.
```

---

## 🌐 2. Arranque del Servidor Web (Uvicorn)

Con el entorno virtual activado, inicie el servidor ASGI con recarga en caliente:

```bash
uvicorn app.main:app --reload
```

Salida típica del servidor:
```text
INFO:     Will watch for changes in these directories: ['C:\\SENSORES INDUSTRIALES']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [67890]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## 📚 3. Documentación Interactiva en el Navegador

Una vez que Uvicorn esté en ejecución, abra su navegador web favorito:

### Swagger UI (Pruebas Interactivas)
* **URL:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Funcionalidad:** Permite inspeccionar cada uno de los 4 endpoints, revisar sus esquemas JSON y ejecutar peticiones directamente con el botón **"Try it out"**.

### ReDoc (Referencia Técnica Formal)
* **URL:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
* **Funcionalidad:** Vista limpia, estructurada y navegable ideal para documentación de referencia y lectura técnica.

---

## 🔌 4. Cómo Cambiar el Puerto si el 8000 está Ocupado

Si otra aplicación ya está utilizando el puerto `8000`, puede indicar un puerto diferente con el parámetro `--port`:

```bash
uvicorn app.main:app --reload --port 8080
```

En este caso, la documentación estará disponible en:
* `http://localhost:8080/docs`

---

## ⏹️ 5. Cómo Apagar el Servidor Correctamente

Para detener la ejecución de la API de forma segura y liberar el puerto:
1. Diríjase a la ventana de la terminal donde está corriendo `uvicorn`.
2. Presione la combinación de teclas: **`Ctrl + C`**.
3. El servidor completará las peticiones en curso y se cerrará limpiamente:
   ```text
   INFO:     Shutting down
   INFO:     Waiting for application shutdown.
   INFO:     Application shutdown complete.
   INFO:     Finished server process [67890]
   ```
