$baseUrl = "http://127.0.0.1:5000"

Write-Host "1. Registering Admin..."
$regBody = @{
    username = "admin_ps"
    password = "password"
    role     = "admin"
} | ConvertTo-Json
$res = Invoke-RestMethod -Uri "$baseUrl/api/auth/register" -Method Post -Body $regBody -ContentType "application/json" -ErrorAction SilentlyContinue
if ($LASTEXITCODE -ne 0) { Write-Host "Register result: $res" }

Write-Host "`n2. Logging in..."
$loginBody = @{
    username = "admin_ps"
    password = "password"
} | ConvertTo-Json
try {
    $res = Invoke-RestMethod -Uri "$baseUrl/api/auth/login" -Method Post -Body $loginBody -ContentType "application/json"
    $token = $res.access_token
    Write-Host "Login successful. Token acquired."
}
catch {
    Write-Host "Login failed: $_"
    exit
}

$headers = @{
    Authorization = "Bearer $token"
}

Write-Host "`n3. Adding Menu Item..."
$itemBody = @{
    name        = "PS Burger"
    price       = 12.50
    category    = "Main"
    description = "Powershell Burger"
} | ConvertTo-Json
try {
    $res = Invoke-RestMethod -Uri "$baseUrl/api/menu/" -Method Post -Body $itemBody -ContentType "application/json" -Headers $headers
    Write-Host "Item Added: $($res.message)"
}
catch {
    Write-Host "Add Item failed: $_"
}

Write-Host "`n4. Getting Menu..."
$menu = Invoke-RestMethod -Uri "$baseUrl/api/menu/" -Method Get
Write-Host "Menu Items count: $(@($menu).Count)"
# Force array
$menuArr = @($menu)
$itemId = [int]$menuArr[0].id
Write-Host "Selected Item ID: $itemId Type: $($itemId.GetType().Name)"

Write-Host "`n5. Placing Order..."
$orderBody = @{
    table_number = 10
    items        = @( @{ menu_item_id = $itemId; quantity = 1 } )
} | ConvertTo-Json -Depth 5
Write-Host "Order Payload: $orderBody"
try {
    $res = Invoke-RestMethod -Uri "$baseUrl/api/orders/" -Method Post -Body $orderBody -ContentType "application/json"
    Write-Host "Order Placed: ID $($res.order_id)"
    $orderId = $res.order_id
}
catch {
    Write-Host "Place Order failed: $_"
    exit
}

Write-Host "`n6. Checking Order Status..."
$order = Invoke-RestMethod -Uri "$baseUrl/api/orders/$orderId" -Method Get
Write-Host "Order Status: $($order.status)"

Write-Host "`n7. Updating Order Status..."
$statusBody = @{ status = "ready" } | ConvertTo-Json
try {
    $res = Invoke-RestMethod -Uri "$baseUrl/api/orders/$orderId/status" -Method Put -Body $statusBody -ContentType "application/json" -Headers $headers
    Write-Host "Status Update: $($res.message)"
}
catch {
    Write-Host "Update failed: $_"
}

Write-Host "`n8. Admin Stats..."
try {
    $stats = Invoke-RestMethod -Uri "$baseUrl/api/admin/stats" -Method Get -Headers $headers
    Write-Host "Total Orders: $($stats.total_orders)"
    Write-Host "Total Sales: $($stats.total_sales)"
}
catch {
    Write-Host "Stats failed: $_"
}
