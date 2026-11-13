"""Suite de pruebas automatizadas con pytest y httpx para la API de Sensores."""
import pytest
from fastapi.testclient import TestClient

from app.database import obtener_coleccion
from app.main import app

cliente = TestClient(app)


@pytest.fixture(autouse=True)
def limpiar_coleccion_pruebas():
    """Fixture que asegura un estado limpio de la colección antes de cada test."""
    coleccion = obtener_coleccion()
    coleccion.delete_many({})
    yield
    # Limpieza posterior opcional
    coleccion.delete_many({})


def test_crear_sensor_valido():
    """Valida la creación exitosa de un sensor con datos correctos (HTTP 201)."""
    payload = {
        "tipo": "temperatura",
        "valor": 25.5,
        "ubicacion": "Planta Central - Sala A",
        "fecha": "2026-11-11T10:00:00",
    }
    respuesta = cliente.post("/sensores/", json=payload)
    assert respuesta.status_code == 201

    datos = respuesta.json()
    assert "id" in datos
    assert datos["tipo"] == "temperatura"
    assert datos["valor"] == 25.5
    assert datos["ubicacion"] == "Planta Central - Sala A"


def test_crear_sensor_tipo_invalido():
    """Valida que un tipo de sensor no admitido sea rechazado con HTTP 422."""
    payload = {
        "tipo": "humedad",  # Tipo no permitido en TipoSensor
        "valor": 55.0,
        "ubicacion": "Invernadero",
        "fecha": "2026-11-11T10:00:00",
    }
    respuesta = cliente.post("/sensores/", json=payload)
    assert respuesta.status_code == 422
    assert "detalle" in respuesta.json() or "detail" in respuesta.json()


def test_crear_sensor_fuera_de_rango():
    """Valida que un valor que exceda los límites del tipo sea rechazado con HTTP 422."""
    payload = {
        "tipo": "presion",
        "valor": 999.0,  # Presión máxima permitida es 500 kPa
        "ubicacion": "Tubería Principal",
        "fecha": "2026-11-11T10:00:00",
    }
    respuesta = cliente.post("/sensores/", json=payload)
    assert respuesta.status_code == 422


def test_listar_sensores():
    """Valida la consulta general de todos los sensores almacenados (HTTP 200)."""
    # Insertar dos sensores
    cliente.post(
        "/sensores/",
        json={
            "tipo": "temperatura",
            "valor": 30.0,
            "ubicacion": "Caldera 1",
            "fecha": "2026-11-11T10:00:00",
        },
    )
    cliente.post(
        "/sensores/",
        json={
            "tipo": "presion",
            "valor": 250.0,
            "ubicacion": "Compresor 2",
            "fecha": "2026-11-11T10:00:00",
        },
    )

    respuesta = cliente.get("/sensores/")
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert isinstance(datos, list)
    assert len(datos) == 2


def test_filtrar_por_tipo():
    """Valida que el query param '?tipo=' filtre adecuadamente los resultados (HTTP 200)."""
    cliente.post(
        "/sensores/",
        json={
            "tipo": "temperatura",
            "valor": 15.0,
            "ubicacion": "Cámara Fría",
            "fecha": "2026-11-11T10:00:00",
        },
    )
    cliente.post(
        "/sensores/",
        json={
            "tipo": "vibracion",
            "valor": 2.1,
            "ubicacion": "Turbina T-1",
            "fecha": "2026-11-11T10:00:00",
        },
    )

    respuesta = cliente.get("/sensores/?tipo=temperatura")
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert len(datos) == 1
    assert datos[0]["tipo"] == "temperatura"


def test_actualizar_sensor_existente():
    """Valida la actualización correcta del primer sensor de un tipo existente (HTTP 200)."""
    cliente.post(
        "/sensores/",
        json={
            "tipo": "temperatura",
            "valor": 20.0,
            "ubicacion": "Silo 1",
            "fecha": "2026-11-11T10:00:00",
        },
    )

    update_payload = {
        "valor": 45.0,
        "ubicacion": "Silo 1 - Módulo Renovado",
    }
    respuesta = cliente.put("/sensores/temperatura", json=update_payload)
    assert respuesta.status_code == 200

    datos = respuesta.json()
    assert datos["valor"] == 45.0
    assert datos["ubicacion"] == "Silo 1 - Módulo Renovado"


def test_actualizar_sensor_inexistente():
    """Valida que intentar actualizar un tipo que no existe retorne HTTP 404."""
    update_payload = {"valor": 20.0, "ubicacion": "Ubicación X"}
    respuesta = cliente.put("/sensores/vibracion", json=update_payload)
    assert respuesta.status_code == 404


def test_eliminar_sensor_existente():
    """Valida la eliminación correcta del primer sensor de un tipo (HTTP 204 sin body)."""
    cliente.post(
        "/sensores/",
        json={
            "tipo": "vibracion",
            "valor": 3.4,
            "ubicacion": "Motor Primario",
            "fecha": "2026-11-11T10:00:00",
        },
    )

    respuesta = cliente.delete("/sensores/vibracion")
    assert respuesta.status_code == 204
    assert respuesta.text == ""

    # Verificar que ya no existe
    consulta = cliente.get("/sensores/?tipo=vibracion")
    assert len(consulta.json()) == 0


def test_eliminar_sensor_inexistente():
    """Valida que intentar eliminar un tipo de sensor que no existe retorne HTTP 404."""
    respuesta = cliente.delete("/sensores/tipo_que_no_existe")
    assert respuesta.status_code == 404
