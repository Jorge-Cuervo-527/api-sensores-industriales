# 🔧 Guía de Solución de Problemas (Troubleshooting)

Esta guía documenta los 8 problemas más comunes que pueden surgir durante el desarrollo, despliegue o evaluación del proyecto, con su causa raíz y la solución paso a paso.

---

### 1. `ConnectionFailure` / `ECONNREFUSED` al intentar conectar con MongoDB

* **Síntoma:** Al arrancar la aplicación o correr tests aparece el mensaje: `pymongo.errors.ServerSelectionTimeoutError: No servers found yet` o `ConnectionFailure`.
* **Causa probable:** El servicio local de MongoDB no está iniciado, o si se utiliza MongoDB Atlas, la IP actual no tiene permisos en Network Access o la máquina no tiene acceso a internet.
* **Solución:**
  * Si usa MongoDB local en Windows: abra PowerShell como Administrador y ejecute `net start MongoDB`.
  * Si usa Linux: ejecute `sudo systemctl start mongod`.
  * Si usa MongoDB Atlas: ingrese a [cloud.mongodb.com](https://cloud.mongodb.com), vaya a **Security -> Network Access** y confirme que exista la regla `0.0.0.0/0` (Allow Access from Anywhere).

---

### 2. `ModuleNotFoundError: No module named 'fastapi'`

* **Síntoma:** Al ejecutar `uvicorn app.main:app --reload` la terminal arroja: `ModuleNotFoundError: No module named 'fastapi'`.
* **Causa probable:** El entorno virtual no ha sido activado o las librerías se instalaron en un intérprete global diferente.
* **Solución:**
  1. Verifique que la terminal tenga el prefijo `(venv)`.
  2. Active el entorno virtual:
     * En Windows: `.\venv\Scripts\activate`
     * En macOS/Linux: `source venv/bin/activate`
  3. Reinstale las dependencias con: `pip install -r requirements.txt`.

---

### 3. `TypeError: ObjectId is not JSON serializable`

* **Síntoma:** La API responde con `HTTP 500` y en los logs aparece `TypeError: Object of type ObjectId is not JSON serializable`.
* **Causa probable:** MongoDB almacena la clave primaria `_id` como un objeto binario BSON `ObjectId`, el cual no puede ser serializado directamente a JSON estándar por FastAPI/JSONResponse.
* **Solución:** La función `serialize()` en `app/main.py` convierte automáticamente `_id` a un string `id`:
  ```python
  if "_id" in doc:
      doc["id"] = str(doc.pop("_id"))
  ```
  Asegúrese de pasar siempre los documentos obtenidos de MongoDB por la función `serialize()` antes de retornarlos en los endpoints.

---

### 4. `Address already in use` (Puerto 8000 ocupado)

* **Síntoma:** Al iniciar `uvicorn` se muestra el error `[Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000): address already in use`.
* **Causa probable:** Hay otra instancia de Uvicorn o algún otro proceso local utilizando el puerto 8000.
* **Solución:**
  * Opción 1: Inicie la API en otro puerto, por ejemplo el 8080:
    ```bash
    uvicorn app.main:app --reload --port 8080
    ```
  * Opción 2: Cierre el proceso que ocupa el puerto en Windows con:
    ```powershell
    Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
    ```

---

### 5. `422 Unprocessable Entity` al hacer `POST /sensores/`

* **Síntoma:** La petición `POST` es rechazada con un código HTTP `422`.
* **Causa probable:** Uno o más campos no cumplen con el esquema de Pydantic v2:
  1. `tipo` no es `temperatura`, `presion` o `vibracion`.
  2. `valor` está fuera del rango permitido (`temperatura`: [-10, 100], `presion`: [0, 500], `vibracion`: [0, 5]).
  3. Falta algún campo obligatorio (`tipo`, `valor`, `ubicacion`, `fecha`).
* **Solución:** Revise la respuesta JSON devuelta por la API; el array `errores` especifica con exactitud el campo y el motivo del rechazo.

---

### 6. `404 Not Found` al hacer `DELETE /sensores/{tipo}` o `PUT /sensores/{tipo}`

* **Síntoma:** Al intentar actualizar o eliminar un sensor se recibe respuesta `HTTP 404`.
* **Causa probable:** No existe ningún documento en la colección de MongoDB cuyo campo `tipo` coincida con el valor pasado en la URL (por ejemplo `/sensores/inexistente` o la colección está vacía).
* **Solución:**
  * Consulte previamente los sensores existentes con `GET /sensores/`.
  * Si la colección fue limpiada, vuelva a poblarla ejecutando: `python scripts/seed_data.py`.

---

### 7. Fecha en formato inválido (`Input should be a valid datetime`)

* **Síntoma:** Se rechaza la petición con error en el campo `fecha`.
* **Causa probable:** La fecha enviada no cumple con el estándar ISO 8601 (`YYYY-MM-DDTHH:MM:SS`).
* **Solución:** Asegúrese de enviar la fecha con la 'T' separadora de fecha y hora, por ejemplo:
  ```json
  "fecha": "2026-11-11T09:30:00"
  ```
  Evite formatos con barras o texto como `11/11/2026 09:30 AM`.

---

### 8. `mongosh: command not found`

* **Síntoma:** Al intentar ejecutar `mongosh` en la terminal, el sistema indica que el comando no es reconocido.
* **Causa probable:** A partir de MongoDB 6.0, la consola interactiva `mongosh` es un paquete separado y no siempre se incluye en el PATH automáticamente durante la instalación.
* **Solución:**
  * En Windows: descargue MongoDB Shell desde [mongodb.com/try/download/shell](https://www.mongodb.com/try/download/shell) y agregue su carpeta `bin` a las Variables de Entorno del Sistema.
  * Alternativa sin `mongosh`: Puede verificar la conectividad directamente desde Python con el comando:
    ```bash
    python -c "from app.database import obtener_cliente; print(obtener_cliente().admin.command('ping'))"
    ```
