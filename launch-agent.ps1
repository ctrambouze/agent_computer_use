# ============================================================
# Lanceur Agent GUI - UI-TARS / Qwen3-VL
# ============================================================

param(
    [string]$Model = "ui-tars",  # ui-tars, qwen3-vl, ou nom complet
    [switch]$CLI,                 # Utiliser Agent TARS CLI au lieu de Desktop
    [switch]$Status               # Afficher le statut uniquement
)

# Configuration
$env:OLLAMA_MODELS = "D:\DATA\ollama\models"
$env:OLLAMA_HOST = "http://127.0.0.1:11434"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Agent GUI Launcher" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Verifier Ollama
$ollamaRunning = Get-Process -Name "ollama*" -ErrorAction SilentlyContinue
if (!$ollamaRunning) {
    Write-Host "`n[*] Demarrage de Ollama..." -ForegroundColor Yellow
    Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 3
}

# Lister les modeles disponibles
Write-Host "`n[*] Modeles disponibles:" -ForegroundColor Yellow
$models = ollama list 2>$null
Write-Host $models

# Resoudre le nom du modele
$modelName = switch ($Model.ToLower()) {
    "ui-tars" { "0000/ui-tars-1.5-7b-q8_0:q8" }
    "qwen" { "qwen3-vl:30b" }
    "qwen3-vl" { "qwen3-vl:30b" }
    "mistral" { "mistral:latest" }
    default { $Model }
}

Write-Host "`n[*] Modele selectionne: $modelName" -ForegroundColor Green

if ($Status) {
    # Afficher le statut et quitter
    Write-Host "`n[*] GPU Status:" -ForegroundColor Yellow
    nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv,noheader
    exit 0
}

if ($CLI) {
    # Lancer Agent TARS CLI avec prompt_engineering pour contourner le probleme des tools
    Write-Host "`n[*] Lancement Agent TARS CLI..." -ForegroundColor Yellow
    Write-Host "    Modele: $modelName" -ForegroundColor Cyan
    Write-Host "    Mode: prompt_engineering (contourne le probleme tools)" -ForegroundColor Cyan
    Write-Host ""
    npx @agent-tars/cli@latest --provider ollama --model $modelName --toolCallEngine prompt_engineering
} else {
    # Instructions pour UI-TARS Desktop
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  Configuration UI-TARS Desktop" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. Ouvrir UI-TARS Desktop" -ForegroundColor White
    Write-Host ""
    Write-Host "2. Aller dans Settings et configurer:" -ForegroundColor White
    Write-Host "   Provider:  Custom/OpenAI-Compatible" -ForegroundColor Gray
    Write-Host "   Base URL:  http://localhost:11434/v1" -ForegroundColor Green
    Write-Host "   API Key:   ollama" -ForegroundColor Green
    Write-Host "   Model:     $modelName" -ForegroundColor Green
    Write-Host ""
    Write-Host "3. Tester avec une mission simple:" -ForegroundColor White
    Write-Host '   "Ouvre Chrome et va sur google.com"' -ForegroundColor Gray
    Write-Host ""

    # Ouvrir le dossier des releases si l'app n'est pas installee
    $desktopApp = Get-ChildItem -Path "C:\Users\$env:USERNAME\AppData\Local\Programs" -Filter "*UI-TARS*" -Directory -ErrorAction SilentlyContinue
    if (!$desktopApp) {
        Write-Host "[!] UI-TARS Desktop non detecte." -ForegroundColor Yellow
        Write-Host "    Telechargez-le depuis: https://github.com/bytedance/UI-TARS-desktop/releases" -ForegroundColor Blue

        $open = Read-Host "Ouvrir la page de telechargement? (O/n)"
        if ($open -ne "n") {
            Start-Process "https://github.com/bytedance/UI-TARS-desktop/releases"
        }
    }
}
