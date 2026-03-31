# ============================================================
# Script de test UI-TARS - Validation du modele local
# ============================================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Test UI-TARS Local" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Verifier que Ollama tourne
Write-Host "`n[1] Verification Ollama..." -ForegroundColor Yellow
$response = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get -ErrorAction SilentlyContinue
if ($response) {
    Write-Host "  Ollama API: OK" -ForegroundColor Green
    Write-Host "  Modeles disponibles:" -ForegroundColor Cyan
    $response.models | ForEach-Object { Write-Host "    - $($_.name)" -ForegroundColor White }
} else {
    Write-Host "  ERREUR: Ollama n'est pas accessible sur localhost:11434" -ForegroundColor Red
    Write-Host "  Lancez: ollama serve" -ForegroundColor Yellow
    exit 1
}

# Test simple avec le modele
Write-Host "`n[2] Test du modele UI-TARS..." -ForegroundColor Yellow

$modelName = "0000/ui-tars-1.5-7b-q8_0:q8"

# Verifier si le modele existe
$modelExists = $response.models | Where-Object { $_.name -like "*ui-tars*" }
if (!$modelExists) {
    Write-Host "  Modele UI-TARS non trouve. Utilisation de avil/UI-TARS..." -ForegroundColor Yellow
    $modelName = "avil/UI-TARS"
}

Write-Host "  Modele utilise: $modelName" -ForegroundColor Cyan

# Test de generation simple
$body = @{
    model = $modelName
    prompt = "What can you do as a GUI automation agent?"
    stream = $false
} | ConvertTo-Json

Write-Host "`n[3] Envoi d'une requete de test..." -ForegroundColor Yellow

try {
    $result = Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 60
    Write-Host "`n  Reponse du modele:" -ForegroundColor Green
    Write-Host "  $($result.response.Substring(0, [Math]::Min(500, $result.response.Length)))..." -ForegroundColor White
    Write-Host "`n  TEST REUSSI!" -ForegroundColor Green
} catch {
    Write-Host "  ERREUR: $($_.Exception.Message)" -ForegroundColor Red
}

# Test API compatible OpenAI
Write-Host "`n[4] Test API compatible OpenAI (pour UI-TARS Desktop)..." -ForegroundColor Yellow

$openaiBody = @{
    model = $modelName
    messages = @(
        @{
            role = "user"
            content = "Hello, are you ready to help with GUI automation?"
        }
    )
} | ConvertTo-Json -Depth 3

try {
    $result = Invoke-RestMethod -Uri "http://localhost:11434/v1/chat/completions" -Method Post -Body $openaiBody -ContentType "application/json" -TimeoutSec 60
    Write-Host "  API OpenAI compatible: OK" -ForegroundColor Green
    Write-Host "  Reponse: $($result.choices[0].message.content.Substring(0, [Math]::Min(200, $result.choices[0].message.content.Length)))..." -ForegroundColor White
} catch {
    Write-Host "  ERREUR API OpenAI: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Tests termines" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
