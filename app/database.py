"""Módulo de configuración y conexión a la base de datos MongoDB."""
import os
from typing import Optional
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import ConnectionFailure, PyMongoError

# Cargar variables de entorno si existe archivo .env local
load_dotenv()

# Variables de configuración con fallback según requisitos de la actividad EA2
MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME: str = os.getenv("DATABASE_NAME", "monitoreo_industrial")
COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "sensores")

_cliente: Optional[MongoClient] = None


def obtener_cliente(uri: Optional[str] = None) -> MongoClient:
    """Obtiene o inicializa la instancia singleton del cliente MongoClient.

    Args:
        uri: URI opcional para conectar a un clúster específico o en pruebas.

    Returns:
        MongoClient: Instancia activa del cliente de MongoDB.

    Raises:
        ConnectionFailure: Si no es posible establecer la conexión con el servidor.
    """
    global _cliente
    cadena_conexion = uri or os.getenv("MONGO_URI", MONGO_URI)
    if _cliente is None:
        try:
            _cliente = MongoClient(cadena_conexion, serverSelectionTimeoutMS=5000)
            # Verificación activa inmediata de conexión mediante comando ping
            _cliente.admin.command("ping")
        except (ConnectionFailure, PyMongoError) as error_conexion:
            _cliente = None
            raise ConnectionFailure(
                f"Error al conectar con MongoDB ({cadena_conexion}): {error_conexion}"
            ) from error_conexion
    return _cliente


def obtener_base_datos() -> Database:
    """Retorna la base de datos configurada para el monitoreo industrial.

    Returns:
        Database: Instancia de la base de datos 'monitoreo_industrial'.
    """
    cliente = obtener_cliente()
    return cliente[DATABASE_NAME]


def obtener_coleccion() -> Collection:
    """Retorna la colección de sensores para operaciones CRUD.

    Returns:
        Collection: Objeto de colección 'sensores' de MongoDB.
    """
    base_datos = obtener_base_datos()
    return base_datos[COLLECTION_NAME]


def get_collection() -> Collection:
    """Alias en inglés para obtener la colección, según especificación del prompt.

    Returns:
        Collection: Objeto de colección 'sensores' de MongoDB.
    """
    return obtener_coleccion()


def cerrar_conexion() -> None:
    """Cierra la conexión con MongoDB y libera los recursos del cliente."""
    global _cliente
    if _cliente is not None:
        _cliente.close()
        _cliente = None
