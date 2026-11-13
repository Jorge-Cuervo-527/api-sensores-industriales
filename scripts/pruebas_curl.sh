#!/usr/bin/env bash
# ==============================================================================
# SCRIPT DE PRUEBAS CON CURL — API MONITOREO DE SENSORES INDUSTRIALES (EA2)
# ==============================================================================
# Secuencia completa de pruebas CRUD para validar el funcionamiento de los endpoints.
# Asegúrate de tener la API corriendo previamente con: uvicorn app.main:app --reload
# ==============================================================================

BASE_URL="http://localhost:8000"

echo "=============================================================================="
echo "🚀 INICIANDO SECUENCIA DE PRUEBAS DE INTEGRACIÓN CON CURL"
echo "=============================================================================="
echo ""

# ------------------------------------------------------------------------------
# 1. POST /sensores/ — Crear un nuevo sensor de prueba (Temperatura)
# ------------------------------------------------------------------------------
echo "👉 1. [POST /sensores/] Creando nuevo sensor de temperatura (201 Created)..."
curl -s -X POST "$BASE_URL/sensores/" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "temperatura",
    "valor": 34.5,
    "ubicacion": "Reactor Químico R-102",
    "fecha": "2026-11-11T09:00:00"
  }' | json_pp 2>/dev/null || cat
echo -e "\n"

# ------------------------------------------------------------------------------
# 2. GET /sensores/ — Listar todos los sensores registrados
# ------------------------------------------------------------------------------
echo "👉 2. [GET /sensores/] Consultando lista completa de sensores (200 OK)..."
curl -s -X GET "$BASE_URL/sensores/" | json_pp 2>/dev/null || cat
echo -e "\n"

# ------------------------------------------------------------------------------
# 3. GET /sensores/?tipo=temperatura — Filtrar sensores por tipo
# ------------------------------------------------------------------------------
echo "👉 3. [GET /sensores/?tipo=temperatura] Filtrando únicamente sensores de temperatura..."
curl -s -X GET "$BASE_URL/sensores/?tipo=temperatura" | json_pp 2>/dev/null || cat
echo -e "\n"

# ------------------------------------------------------------------------------
# 4. PUT /sensores/temperatura — Actualizar el primer sensor de temperatura
# ------------------------------------------------------------------------------
echo "👉 4. [PUT /sensores/temperatura] Modificando valor y ubicación del sensor (200 OK)..."
curl -s -X PUT "$BASE_URL/sensores/temperatura" \
  -H "Content-Type: application/json" \
  -d '{
    "valor": 48.2,
    "ubicacion": "Reactor Químico R-102 - Módulo Actualizado",
    "fecha": "2026-11-11T09:30:00"
  }' | json_pp 2>/dev/null || cat
echo -e "\n"

# ------------------------------------------------------------------------------
# 5. GET /sensores/?tipo=temperatura — Verificar que la actualización surtió efecto
# ------------------------------------------------------------------------------
echo "👉 5. [GET /sensores/?tipo=temperatura] Comprobando la actualización aplicada..."
curl -s -X GET "$BASE_URL/sensores/?tipo=temperatura" | json_pp 2>/dev/null || cat
echo -e "\n"

# ------------------------------------------------------------------------------
# 6. DELETE /sensores/temperatura — Eliminar el primer sensor de temperatura
# ------------------------------------------------------------------------------
echo "👉 6. [DELETE /sensores/temperatura] Eliminando el sensor de temperatura (204 No Content)..."
STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "$BASE_URL/sensores/temperatura")
echo "Código de estado HTTP obtenido: $STATUS_CODE"
echo -e "\n"

# ------------------------------------------------------------------------------
# 7. GET /sensores/ — Verificar el estado final tras la eliminación
# ------------------------------------------------------------------------------
echo "👉 7. [GET /sensores/] Verificando estado final de la colección..."
curl -s -X GET "$BASE_URL/sensores/" | json_pp 2>/dev/null || cat
echo -e "\n"

# ------------------------------------------------------------------------------
# 8. Casos de error esperados (Validación 422 y No Encontrado 404)
# ------------------------------------------------------------------------------
echo "👉 8.1 [POST /sensores/] Probando tipo inválido (Espera HTTP 422)..."
curl -s -X POST "$BASE_URL/sensores/" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "humedad",
    "valor": 50.0,
    "ubicacion": "Bodega 3",
    "fecha": "2026-11-11T09:00:00"
  }' | json_pp 2>/dev/null || cat
echo -e "\n"

echo "👉 8.2 [POST /sensores/] Probando valor fuera de rango (Espera HTTP 422)..."
curl -s -X POST "$BASE_URL/sensores/" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "presion",
    "valor": 999.0,
    "ubicacion": "Línea Alta Presión",
    "fecha": "2026-11-11T09:00:00"
  }' | json_pp 2>/dev/null || cat
echo -e "\n"

echo "👉 8.3 [DELETE /sensores/inexistente] Probando eliminación de tipo inexistente (Espera HTTP 404)..."
curl -s -X DELETE "$BASE_URL/sensores/inexistente" | json_pp 2>/dev/null || cat
echo -e "\n"

echo "=============================================================================="
echo "✅ SECUENCIA DE PRUEBAS COMPLETADA"
echo "=============================================================================="
