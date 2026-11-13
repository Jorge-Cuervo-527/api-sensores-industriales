# ⚙️ Guía de Instalación y Configuración del Entorno

Esta guía detalla el proceso completo para preparar el entorno de ejecución del proyecto **EA2: API CRUD con MongoDB**, soportando los principales sistemas operativos (Windows, macOS y Linux) así como la opción de conexión en la nube mediante MongoDB Atlas.

---

## 📋 Requisitos Previos

* **Python 3.10 o superior** (verificado con Python 3.11.9).
* **MongoDB Community Server 6.0+** (local) O una cuenta en **MongoDB Atlas** (en la nube).
* **Gestor de paquetes `pip`** actualizado.
* Conexión a Internet para la descarga de dependencias.

---

## 🖥️ 1. Instalación de Python 3.10+

### Windows
1. Descargue el instalador oficial desde [python.org/downloads](https://www.python.org/downloads/).
2. Ejecute el instalador `.exe`.
3. ⚠️ **MUY IMPORTANTE:** Marque la casilla **"Add python.exe to PATH"** antes de presionar *Install Now*.
4. Verifique en PowerShell o CMD:
   ```powershell
   python --version
   ```

### macOS
1. Mediante Homebrew:
   ```bash
   brew install python@3.11
   ```
2. Verifique en la terminal:
   ```bash
   python3 --version
   ```

### Linux (Ubuntu / Debian)
1. Actualice los repositorios e instale Python y `venv`:
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-pip python3-venv
   ```
2. Verifique la versión:
   ```bash
   python3 --version
   ```

---

## 🍃 2. Instalación y Configuración de MongoDB

Tienes dos alternativas para la base de datos: **Local (MongoDB Community)** o **Nube (MongoDB Atlas)**. Ambas son 100% compatibles con esta API.

### Opción A: MongoDB Community Local

#### En Windows
1. Descargue el instalador MSI desde el [Centro de Descargas de MongoDB Community](https://www.mongodb.com/try/download/community).
2. Ejecute el instalador:
   * Seleccione **Complete**.
   * Asegúrese de marcar **"Install MongoD as a Service"** y **"Run service as Network Service user"**.
   * Opcionalmente marque **"Install MongoDB Compass"** (herramienta gráfica muy útil).
3. Inicie el servicio desde una terminal con privilegios de Administrador si no arrancó automáticamente:
   ```powershell
   net start MongoDB
   ```
4. Compruebe la conectividad mediante `mongosh`:
   ```powershell
   mongosh --eval "db.runCommand({ ping: 1 })"
   ```

#### En macOS (Homebrew)
```bash
brew tap mongodb/brew
brew install mongodb-community@7.0
brew services start mongodb-community@7.0
mongosh --eval "db.runCommand({ ping: 1 })"
```

#### En Linux (Ubuntu / Debian)
```bash
sudo apt-get install gnupg curl
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
mongosh --eval "db.runCommand({ ping: 1 })"
```

---

### Opción B: MongoDB Atlas (En la Nube — Sin Instalación Local)
1. Regístrese gratuitamente en [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas/register).
2. Cree un clúster gratuito **M0 Free Tier** (proveedor AWS / Azure / GCP).
3. En la sección **Security -> Database Access**, cree un usuario y contraseña (ejemplo: `usuario_sensor` / `ClaveSegura2026`).
4. En **Security -> Network Access**, agregue una regla para permitir acceso desde cualquier IP: `0.0.0.0/0`.
5. En la pestaña del clúster, presione **Connect -> Drivers -> Python** y copie la cadena de conexión.
6. Guarde esa URI en el archivo `.env` del proyecto:
   ```env
   MONGO_URI="mongodb+srv://usuario_sensor:ClaveSegura2026@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
   DATABASE_NAME="monitoreo_industrial"
   COLLECTION_NAME="sensores"
   ```

---

## 💻 3. Instalación de MongoDB Compass (Opcional)

MongoDB Compass es la interfaz gráfica oficial para explorar documentos, colecciones e índices:
* Descarga gratuita: [mongodb.com/products/tools/compass](https://www.mongodb.com/products/tools/compass).
* Para conectar:
  * Local: `mongodb://localhost:27017`
  * Nube: pegue la misma URI de MongoDB Atlas configurada en su `.env`.

---

## 🐍 4. Configuración del Proyecto y Entorno Virtual

1. Abra una terminal en la raíz del proyecto (`c:\SENSORES INDUSTRIALES`):
   ```bash
   cd c:\SENSORES INDUSTRIALES
   ```

2. Cree el entorno virtual de Python:
   * **Windows:**
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   * **macOS / Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Instale las dependencias exactas especificadas en `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

---

## ✅ 5. Verificación Final de la Instalación

Compruebe que las librerías críticas importan correctamente ejecutando este comando de una sola línea:

```bash
python -c "import fastapi, pymongo, pydantic, pytest, httpx; print('✅ INSTALACIÓN VERIFICADA EXITOSAMENTE')"
```

Salida esperada:
```text
✅ INSTALACIÓN VERIFICADA EXITOSAMENTE
```

¡El entorno está completamente preparado para operar la API!
