"""Aplicación principal FastAPI para la gestión de sensores industriales."""
from typing import Any, Optional
from fastapi import FastAPI, HTTPException, Query, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import get_redoc_html
from pymongo.errors import PyMongoError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import HTMLResponse

from app.database import obtener_coleccion
from app.errors import (
    manejador_error_general,
    manejador_http_exception,
    manejador_pymongo_error,
    manejador_validacion_error,
)
from app.models import SensorCreate, SensorOut, SensorUpdate

# URL de ReDoc con versión estable (evita @next que puede estar rota)
REDOC_JS_URL = "https://cdn.jsdelivr.net/npm/redoc@2.1.5/bundles/redoc.standalone.js"

# Instancia de la aplicación FastAPI con metadatos descriptivos
# Se desactiva la ruta de redoc por defecto para reemplazarla con versión estable
app = FastAPI(
    title="EA2 API Sensores",
    description="API RESTful para la gestión y monitoreo de sensores industriales (CRUD).",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,
)


@app.get("/redoc", include_in_schema=False)
async def redoc_html() -> HTMLResponse:
    """Sirve la documentación ReDoc con una versión estable del script JS."""
    return get_redoc_html(
        openapi_url=app.openapi_url or "/openapi.json",
        title=app.title + " - ReDoc",
        redoc_js_url=REDOC_JS_URL,
    )

# Registro centralizado de manejadores de excepciones
app.add_exception_handler(PyMongoError, manejador_pymongo_error)
app.add_exception_handler(StarletteHTTPException, manejador_http_exception)
app.add_exception_handler(RequestValidationError, manejador_validacion_error)
app.add_exception_handler(Exception, manejador_error_general)


def serialize(doc: dict[str, Any]) -> dict[str, Any]:
    """Serializa un documento BSON de MongoDB convirtiendo '_id' en 'id' string.

    Args:
        doc: Diccionario obtenido de MongoDB.

    Returns:
        dict[str, Any]: Diccionario con la clave 'id' en formato string y sin '_id'.
    """
    if not doc:
        return {}
    documento = dict(doc)
    if "_id" in documento:
        documento["id"] = str(documento.pop("_id"))
    return documento


# Alias descriptivo en español
serializar_sensor = serialize


@app.get(
    "/",
    tags=["General"],
    summary="Ruta de bienvenida",
    description="Comprueba el estado de la API y proporciona enlaces a la documentación.",
)
def inicio() -> dict[str, str]:
    """Retorna un mensaje de bienvenida y estado operativo."""
    return {
        "mensaje": "Bienvenido a la API de Monitoreo de Sensores Industriales (EA2)",
        "documentacion": "/docs",
        "redoc": "/redoc",
    }


@app.post(
    "/sensores/",
    response_model=SensorOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Sensores"],
    summary="Crear sensor",
    description="Registra una nueva lectura de sensor tras validar su tipo y rango admisible.",
)
def crear_sensor(sensor: SensorCreate) -> dict[str, Any]:
    """Inserta un nuevo sensor en la colección y retorna el documento creado.

    Args:
        sensor: Datos validados del nuevo sensor a registrar.

    Returns:
        dict[str, Any]: Documento del sensor recién insertado con su 'id'.
    """
    coleccion = obtener_coleccion()
    datos_sensor = sensor.model_dump()
    resultado = coleccion.insert_one(datos_sensor)
    datos_sensor["_id"] = resultado.inserted_id
    return serialize(datos_sensor)


@app.get(
    "/sensores/",
    response_model=list[SensorOut],
    status_code=status.HTTP_200_OK,
    tags=["Sensores"],
    summary="Listar sensores",
    description="Lista todos los sensores o filtra por el parámetro de consulta 'tipo'.",
)
def listar_sensores(
    tipo: Optional[str] = Query(
        default=None,
        description="Filtro opcional por tipo de sensor ('temperatura', 'presion', 'vibracion')",
    )
) -> list[dict[str, Any]]:
    """Obtiene los sensores almacenados, aplicando filtro por tipo si fue proporcionado.

    Args:
        tipo: Tipo de sensor por el cual filtrar las lecturas.

    Returns:
        list[dict[str, Any]]: Lista de sensores serializados.
    """
    coleccion = obtener_coleccion()
    filtro: dict[str, Any] = {}
    if tipo:
        filtro["tipo"] = tipo
    documentos = list(coleccion.find(filtro))
    return [serialize(doc) for doc in documentos]


@app.put(
    "/sensores/{tipo}",
    response_model=SensorOut,
    status_code=status.HTTP_200_OK,
    tags=["Sensores"],
    summary="Actualizar sensor por tipo",
    description="Actualiza el primer sensor encontrado del tipo especificado.",
)
def actualizar_sensor(tipo: str, datos_actualizacion: SensorUpdate) -> dict[str, Any]:
    """Actualiza los datos del primer sensor coincidente con el tipo indicado.

    Args:
        tipo: Tipo de sensor a actualizar ('temperatura', 'presion', 'vibracion').
        datos_actualizacion: Campos a actualizar con sus nuevos valores.

    Returns:
        dict[str, Any]: Documento actualizado serializado.

    Raises:
        HTTPException: 404 si no existe un sensor del tipo dado.
        HTTPException: 422 si el valor actualizado está fuera del rango permitido.
    """
    coleccion = obtener_coleccion()
    sensor_existente = coleccion.find_one({"tipo": tipo})
    if not sensor_existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró ningún sensor de tipo '{tipo}' para actualizar.",
        )

    # Validar que el nuevo valor cumpla con el rango del tipo de sensor
    if datos_actualizacion.valor is not None:
        try:
            datos_actualizacion.validar_contra_tipo(tipo)
        except ValueError as error_rango:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(error_rango),
            ) from error_rango

    campos_a_actualizar = {
        k: v for k, v in datos_actualizacion.model_dump().items() if v is not None
    }

    if campos_a_actualizar:
        coleccion.update_one(
            {"_id": sensor_existente["_id"]},
            {"$set": campos_a_actualizar},
        )
        sensor_actualizado = coleccion.find_one({"_id": sensor_existente["_id"]})
        return serialize(sensor_actualizado or sensor_existente)

    return serialize(sensor_existente)


@app.delete(
    "/sensores/{tipo}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Sensores"],
    summary="Eliminar sensor por tipo",
    description="Elimina el primer sensor encontrado del tipo especificado.",
)
def eliminar_sensor(tipo: str) -> Response:
    """Elimina el primer sensor del tipo indicado de la base de datos.

    Args:
        tipo: Tipo de sensor a eliminar ('temperatura', 'presion', 'vibracion').

    Returns:
        Response: Respuesta HTTP 204 sin contenido.

    Raises:
        HTTPException: 404 si no existe ningún sensor del tipo dado.
    """
    coleccion = obtener_coleccion()
    documento_eliminado = coleccion.find_one_and_delete({"tipo": tipo})
    if not documento_eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró ningún sensor de tipo '{tipo}' para eliminar.",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
