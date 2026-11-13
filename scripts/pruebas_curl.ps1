# ==============================================================================
# SCRIPT DE PRUEBAS PARA WINDOWS / POWERSHELL — API MONITOREO SENSORES (EA2)
# ==============================================================================
$BaseUrl = "http://localhost:8000"

Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host "🚀 INICIANDO SECUENCIA DE PRUEBAS EN POWERSHELL CON CURL.EXE" -ForegroundColor Cyan
Write-Host "==============================================================================" -ForegroundColor Cyan

# 1. POST
Write-Host "`n👉 1. [POST /sensores/] Creando sensor de temperatura (201 Created)..." -ForegroundColor Yellow
curl.exe -s -X POST "$BaseUrl/sensores/" -H "Content-Type: application/json" -d '{\"tipo\": \"temperatura\", \"valor\": 34.5, \"ubicacion\": \"Reactor Quimico R-102\", \"fecha\": \"2026-11-11T09:00:00\"}'
Write-Host ""

# 2. GET todos
Write-Host "`n👉 2. [GET /sensores/] Consultando lista completa de sensores (200 OK)..." -ForegroundColor Yellow
curl.exe -s -X GET "$BaseUrl/sensores/"
Write-Host ""

# 3. GET filtrado
Write-Host "`n👉 3. [GET /sensores/?tipo=temperatura] Filtrando por tipo 'temperatura'..." -ForegroundColor Yellow
curl.exe -s -X GET "$BaseUrl/sensores/?tipo=temperatura"
Write-Host ""

# 4. PUT
Write-Host "`n👉 4. [PUT /sensores/temperatura] Modificando valor y ubicacion (200 OK)..." -ForegroundColor Yellow
curl.exe -s -X PUT "$BaseUrl/sensores/temperatura" -H "Content-Type: application/json" -d '{\"valor\": 48.2, \"ubicacion\": \"Reactor Quimico R-102 - Modulo Actualizado\"}'
Write-Host ""

# 5. GET de comprobación
Write-Host "`n👉 5. [GET /sensores/?tipo=temperatura] Comprobando actualizacion..." -ForegroundColor Yellow
curl.exe -s -X GET "$BaseUrl/sensores/?tipo=temperatura"
Write-Host ""

# 6. DELETE
Write-Host "`n👉 6. [DELETE /sensores/temperatura] Eliminando sensor (204 No Content)..." -ForegroundColor Yellow
$status = curl.exe -s -o NUL -w "%{http_code}" -X DELETE "$BaseUrl/sensores/temperatura"
Write-Host "Codigo HTTP devuelto: $status" -ForegroundColor Green

# 7. GET final
Write-Host "`n👉 7. [GET /sensores/] Estado final tras la eliminacion..." -ForegroundColor Yellow
curl.exe -s -X GET "$BaseUrl/sensores/"
Write-Host ""

# 8. Casos de error
Write-Host "`n👉 8.1 Error 422 (Tipo invalido):" -ForegroundColor Red
curl.exe -s -X POST "$BaseUrl/sensores/" -H "Content-Type: application/json" -d '{\"tipo\": \"humedad\", \"valor\": 50.0, \"ubicacion\": \"Bodega\", \"fecha\": \"2026-11-11T09:00:00\"}'
Write-Host ""

Write-Host "`n👉 8.2 Error 422 (Valor fuera de rango):" -ForegroundColor Red
curl.exe -s -X POST "$BaseUrl/sensores/" -H "Content-Type: application/json" -d '{\"tipo\": \"presion\", \"valor\": 999.0, \"ubicacion\": \"Linea\", \"fecha\": \"2026-11-11T09:00:00\"}'
Write-Host ""

Write-Host "`n👉 8.3 Error 404 (Eliminar tipo inexistente):" -ForegroundColor Red
curl.exe -s -X DELETE "$BaseUrl/sensores/inexistente"
Write-Host ""

Write-Host "`n==============================================================================" -ForegroundColor Cyan
Write-Host "✅ SECUENCIA DE PRUEBAS EN POWERSHELL COMPLETADA CON EXITO" -ForegroundColor Cyan
Write-Host "==============================================================================" -ForegroundColor Cyan
