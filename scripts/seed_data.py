"""Script para poblar la base de datos con sensores industriales de ejemplo."""
import os
import sys
from datetime import datetime, timezone

# Asegurar que el directorio raíz del proyecto esté en el sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import obtener_coleccion

# Datos de prueba realistas para cada tipo de sensor
SENSORES_SEMILLA = [
    {
        "tipo": "temperatura",
        "valor": 23.8,
        "ubicacion": "Horno de Secado - Nave A",
        "fecha": datetime(2026, 11, 11, 8, 0, 0, tzinfo=timezone.utc),
    },
    {
        "tipo": "presion",
        "valor": 175.5,
        "ubicacion": "Compresor Principal - Sala de Máquinas",
        "fecha": datetime(2026, 11, 11, 8, 15, 0, tzinfo=timezone.utc),
    },
    {
        "tipo": "vibracion",
        "valor": 1.45,
        "ubicacion": "Bomba Centrífuga B-101 - Sector Oeste",
        "fecha": datetime(2026, 11, 11, 8, 30, 0, tzinfo=timezone.utc),
    },
]


def poblar_datos() -> None:
    """Inserta los sensores de prueba en la colección de MongoDB."""
    print("=" * 60)
    print("🌱 INICIANDO CARGA DE DATOS DE EJEMPLO (SEED)...")
    print("=" * 60)

    coleccion = obtener_coleccion()

    # Opcional: limpiar registros previos para evitar duplicidad masiva
    resultado_limpieza = coleccion.delete_many({})
    print(f"🧹 Registros anteriores eliminados: {resultado_limpieza.deleted_count}")

    # Insertar los 3 sensores de ejemplo
    resultado = coleccion.insert_many(SENSORES_SEMILLA)

    print(f"✅ Se insertaron exitosamente {len(resultado.inserted_ids)} sensores:")
    for sensor, sensor_id in zip(SENSORES_SEMILLA, resultado.inserted_ids):
        print(f"  • [{sensor['tipo'].upper()}] - ID: {sensor_id}")
        print(f"    Valor: {sensor['valor']} | Ubicación: {sensor['ubicacion']}")
        print(f"    Fecha: {sensor['fecha'].isoformat()}\n")

    print("✨ Carga de datos completada con éxito.")


if __name__ == "__main__":
    poblar_datos()
