# 📑 Reporte Final de Validación del Proyecto (EA2)

**Actividad:** EA2 — Bases de datos NoSQL y operaciones CRUD  
**Proyecto:** API RESTful para Monitoreo de Sensores Industriales  
**Tecnologías:** FastAPI, MongoDB, Pydantic v2, PyMongo, Pytest  
**Fecha:** Noviembre 2026  
**Resultado de Validación:** ✅ **100% APROBADO (Todos los criterios superados)**

---

## 1. Registro de Comandos Ejecutados y Salidas Reales

### 1.1 Inserción de Datos Iniciales (`seed_data.py`)
```bash
python scripts/seed_data.py
```
**Salida de consola obtenida:**
```text
============================================================
🌱 INICIANDO CARGA DE DATOS DE EJEMPLO (SEED)...
============================================================
🧹 Registros anteriores eliminados: 0
✅ Se insertaron exitosamente 3 sensores:
  • [TEMPERATURA] - ID: 6af470c6820f7cba3820ab92
    Valor: 23.8 | Ubicación: Horno de Secado - Nave A
    Fecha: 2026-11-11T08:00:00+00:00

  • [PRESION] - ID: 6af470c6820f7cba3820ab93
    Valor: 175.5 | Ubicación: Compresor Principal - Sala de Máquinas
    Fecha: 2026-11-11T08:15:00+00:00

  • [VIBRACION] - ID: 6af470c6820f7cba3820ab94
    Valor: 1.45 | Ubicación: Bomba Centrífuga B-101 - Sector Oeste
    Fecha: 2026-11-11T08:30:00+00:00

✨ Carga de datos completada con éxito.
```

---

### 1.2 Ejecución de Suite de Pruebas Unitarias y de Integración (`pytest`)
```bash
pytest tests/ -v
```
**Salida de consola obtenida:**
```text
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-8.3.3, pluggy-1.7.0 -- C:\SENSORES INDUSTRIALES\venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\SENSORES INDUSTRIALES
plugins: anyio-4.16.0
collecting ... collected 9 items

tests/test_api.py::test_crear_sensor_valido PASSED                       [ 11%]
tests/test_api.py::test_crear_sensor_tipo_invalido PASSED                [ 22%]
tests/test_api.py::test_crear_sensor_fuera_de_rango PASSED               [ 33%]
tests/test_api.py::test_listar_sensores PASSED                           [ 44%]
tests/test_api.py::test_filtrar_por_tipo PASSED                          [ 55%]
tests/test_api.py::test_actualizar_sensor_existente PASSED               [ 66%]
tests/test_api.py::test_actualizar_sensor_inexistente PASSED             [ 77%]
tests/test_api.py::test_eliminar_sensor_existente PASSED                 [ 88%]
tests/test_api.py::test_eliminar_sensor_inexistente PASSED               [100%]

======================== 9 passed, 1 warning in 4.25s =========================
```

---

### 1.3 Secuencia Completa de Pruebas CRUD (`curl` / PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -File scripts/pruebas_curl.ps1
```
**Respuestas HTTP verificadas:**
* **POST `/sensores/`:** Retorna código `201 Created` y el objeto creado con su `id` BSON serializado.
* **GET `/sensores/`:** Retorna código `200 OK` con la lista de los 3 sensores.
* **GET `/sensores/?tipo=temperatura`:** Retorna código `200 OK` con filtrado exacto.
* **PUT `/sensores/temperatura`:** Retorna código `200 OK` reflejando el nuevo valor y ubicación.
* **DELETE `/sensores/temperatura`:** Retorna código `204 No Content` sin cuerpo.
* **POST `/sensores/` con tipo inválido:** Retorna código `422 Unprocessable Entity` (`Input should be 'temperatura', 'presion' or 'vibracion'`).
* **POST `/sensores/` con valor fuera de rango:** Retorna código `422 Unprocessable Entity` (`Value error, El valor para 'presion' debe estar entre 0.0 y 500.0.`).
* **DELETE `/sensores/inexistente`:** Retorna código `404 Not Found` (`No se encontró ningún sensor de tipo 'inexistente' para eliminar.`).

---

## 📸 2. Guía de Capturas de Pantalla Recomendadas para la Entrega

Para la sustentación de la actividad ante el docente o evaluador, se sugiere tomar las siguientes 6 capturas de pantalla:

1. **Captura 1 — Estructura del Proyecto en el Editor:**
   * Mostrar el explorador de archivos con las carpetas `app/`, `tests/`, `scripts/`, `docs/` y los archivos de configuración.
2. **Captura 2 — Swagger UI en el Navegador:**
   * Abrir `http://localhost:8000/docs` mostrando los 4 endpoints CRUD desplegados con sus etiquetas y modelos.
3. **Captura 3 — Petición POST Exitosa (Postman o Swagger):**
   * Mostrar el envío del body JSON y la respuesta `201 Created` con el campo `id`.
4. **Captura 4 — Validación 422 (Tipo Inválido o Valor Fuera de Rango):**
   * Mostrar el rechazo inmediato de una lectura incorrecta con `HTTP 422` y el mensaje en español.
5. **Captura 5 — Eliminación y Respuesta 204:**
   * Mostrar la petición `DELETE /sensores/temperatura` con código `204 No Content`.
6. **Captura 6 — Pruebas Automatizadas en Consola:**
   * Mostrar la terminal ejecutando `pytest tests/ -v` con los 9 tests en verde (`PASSED`).

---

## ✅ 3. Matriz de Cumplimiento de Criterios de Aceptación

| Criterio de Aceptación | Estado | Observación |
|---|:---:|---|
| Los 14 archivos existen en las rutas correctas | ✅ CUMPLE | Toda la estructura fue creada según el árbol formal. |
| `pip install -r requirements.txt` instala sin errores | ✅ CUMPLE | Dependencias fijadas instaladas limpiamente en `venv`. |
| `uvicorn app.main:app --reload` arranca sin warnings | ✅ CUMPLE | Servidor ASGI inicia y responde en `http://localhost:8000/`. |
| Swagger UI carga en `http://localhost:8000/docs` con 4 endpoints | ✅ CUMPLE | Documentación OpenAPI interactiva disponible. |
| Los 4 endpoints responden con los códigos HTTP correctos | ✅ CUMPLE | 201 en POST, 200 en GET/PUT, 204 en DELETE. |
| Validación rechaza `tipo="humedad"` con HTTP 422 | ✅ CUMPLE | Verificado por Pydantic v2 en `test_crear_sensor_tipo_invalido`. |
| Validación rechaza `presion=999` con HTTP 422 (máx 500) | ✅ CUMPLE | Verificado por `@field_validator` en `test_crear_sensor_fuera_de_rango`. |
| `DELETE /sensores/inexistente` responde HTTP 404 | ✅ CUMPLE | Verificado en `test_eliminar_sensor_inexistente`. |
| `pytest tests/ -v` muestra todos los tests en verde (mínimo 8) | ✅ CUMPLE | 9 tests implementados y aprobados (100% pass). |
| Los 7 archivos `.md` tienen contenido completo (sin placeholders) | ✅ CUMPLE | Redacción exhaustiva, diagramas y tablas en `docs/`. |
| Código comentado en español con Google docstrings y type hints | ✅ CUMPLE | Convenciones PEP 8, PEP 484 y estilo profesional. |
| Sin `TODO`, `FIXME` ni bloques `pass` vacíos | ✅ CUMPLE | Código de producción limpio y finalizado. |
| Empaquetado final `.zip` excluye `venv/` y cachés | ✅ CUMPLE | Empaquetado limpio generado mediante script. |
