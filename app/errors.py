"""Manejadores centralizados de excepciones y respuestas de error en español."""
import logging
from typing import Any
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pymongo.errors import PyMongoError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("api_sensores")


async def manejador_pymongo_error(request: Request, exc: PyMongoError) -> JSONResponse:
    """Captura fallos de PyMongo y responde con HTTP 500 genérico sin exponer detalles internos.

    Args:
        request: Objeto de la petición entrante.
        exc: Excepción de PyMongo capturada.

    Returns:
        JSONResponse: Respuesta HTTP 500 con mensaje genérico en español.
    """
    logger.error("Error en operación con base de datos MongoDB: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detalle": "Error interno del servidor al procesar la operación en la base de datos."
        },
    )


async def manejador_http_exception(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """Captura excepciones HTTP estándar para garantizar una respuesta uniforme.

    Args:
        request: Objeto de la petición entrante.
        exc: Excepción HTTP lanzada.

    Returns:
        JSONResponse: Respuesta con el código de estado correspondiente y mensaje en 'detalle'.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detalle": exc.detail},
    )


async def manejador_validacion_error(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Captura errores de validación de Pydantic v2 y responde con HTTP 422 detallado.

    Args:
        request: Objeto de la petición entrante.
        exc: Excepción de validación de FastAPI / Pydantic.

    Returns:
        JSONResponse: Respuesta HTTP 422 con desglose claro de campos inválidos.
    """
    errores_detallados: list[dict[str, Any]] = []
    for error in exc.errors():
        ubicacion = " -> ".join(str(loc) for loc in error.get("loc", []))
        mensaje = error.get("msg", "Error de validación")
        errores_detallados.append({
            "campo": ubicacion,
            "mensaje": mensaje,
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detalle": "Los datos enviados no pasaron las validaciones requeridas.",
            "errores": errores_detallados,
        },
    )


async def manejador_error_general(request: Request, exc: Exception) -> JSONResponse:
    """Captura cualquier excepción no controlada respondiendo con HTTP 500 genérico.

    Args:
        request: Objeto de la petición entrante.
        exc: Excepción no controlada.

    Returns:
        JSONResponse: Respuesta HTTP 500 sin exponer el stacktrace al cliente.
    """
    logger.error("Excepción no controlada en la aplicación: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detalle": "Ocurrió un error interno no previsto en el servidor."},
    )
