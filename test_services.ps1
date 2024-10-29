# Test de servicios
Write-Host "Probando servicios..." -ForegroundColor Green

# Test Servicio de Usuarios
$usersResponse = Invoke-RestMethod -Uri "http://localhost:5000/api/usuarios" -Method Get
Write-Host "`nServicio de Usuarios:" -ForegroundColor Yellow
$usersResponse.data | ConvertTo-Json

# Test Servicio de Pedidos
$ordersResponse = Invoke-RestMethod -Uri "http://localhost:5001/api/pedidos" -Method Get
Write-Host "`nServicio de Pedidos:" -ForegroundColor Yellow
$ordersResponse.data | ConvertTo-Json

# Test de integración
Write-Host "`nProbando integración..." -ForegroundColor Green
$userOrders = Invoke-RestMethod -Uri "http://localhost:5001/api/pedidos/1" -Method Get
Write-Host "Pedidos del usuario 1:" -ForegroundColor Yellow
$userOrders.data | ConvertTo-Json