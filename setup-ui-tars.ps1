# ============================================================
# UI-TARS Agent Setup Script for Windows + RTX 3090
# Logiciels: C: | Donnees: D:
# ============================================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  UI-TARS Agent Setup - RTX 3090" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# --- ETAPE 1: Verification des prerequis ---
Write-Host "`n[1/6] Verification des prerequis..." -ForegroundColor Yellow

# Check NVIDIA GPU
$gpu = nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>$null
if ($gpu) {
    Write-Host "  GPU detecte: $gpu" -ForegroundColor Green
} else {
    Write-Host "  ERREUR: GPU NVIDIA non detecte!" -ForegroundColor Red
    exit 1
}

# Check Ollama
$ollamaVersion = ollama --version 2>$null
if ($ollamaVersion) {
    Write-Host "  Ollama: $ollamaVersion" -ForegroundColor Green
} else {
    Write-Host "  ERREUR: Ollama non installe!" -ForegroundColor Red
    Write-Host "  Telecharger depuis: https://ollama.com/download/windows" -ForegroundColor Yellow
    exit 1
}

# Check Node.js
$nodeVersion = node --version 2>$null
if ($nodeVersion) {
    Write-Host "  Node.js: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "  ATTENTION: Node.js non installe (optionnel pour Agent TARS CLI)" -ForegroundColor Yellow
}

# --- ETAPE 2: Configuration Ollama pour stocker les modeles sur D: ---
Write-Host "`n[2/6] Configuration Ollama (modeles sur D:)..." -ForegroundColor Yellow

$modelsPath = "D:\DATA\ollama\models"
if (!(Test-Path $modelsPath)) {
    New-Item -ItemType Directory -Path $modelsPath -Force | Out-Null
    Write-Host "  Dossier cree: $modelsPath" -ForegroundColor Green
}

# Set environment variable permanently
$currentValue = [Environment]::GetEnvironmentVariable("OLLAMA_MODELS", "User")
if ($currentValue -ne $modelsPath) {
    [Environment]::SetEnvironmentVariable("OLLAMA_MODELS", $modelsPath, "User")
    $env:OLLAMA_MODELS = $modelsPath
    Write-Host "  Variable OLLAMA_MODELS definie: $modelsPath" -ForegroundColor Green
    Write-Host "  IMPORTANT: Redemarrez votre terminal apres ce script!" -ForegroundColor Yellow
} else {
    Write-Host "  OLLAMA_MODELS deja configure: $modelsPath" -ForegroundColor Green
}

# --- ETAPE 3: Demarrer Ollama si pas deja lance ---
Write-Host "`n[3/6] Verification du serveur Ollama..." -ForegroundColor Yellow

$ollamaRunning = Get-Process -Name "ollama*" -ErrorAction SilentlyContinue
if (!$ollamaRunning) {
    Write-Host "  Demarrage de Ollama..." -ForegroundColor Yellow
    Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 3
    Write-Host "  Ollama demarre" -ForegroundColor Green
} else {
    Write-Host "  Ollama deja en cours d'execution" -ForegroundColor Green
}

# --- ETAPE 4: Telecharger le modele UI-TARS ---
Write-Host "`n[4/6] Telechargement du modele UI-TARS 1.5 7B Q8..." -ForegroundColor Yellow
Write-Host "  Taille: ~8.1 GB - Cela peut prendre plusieurs minutes" -ForegroundColor Yellow

# Pull le modele UI-TARS 1.5 quantifie Q8 (meilleure qualite pour RTX 3090)
ollama pull 0000/ui-tars-1.5-7b-q8_0:q8

if ($LASTEXITCODE -eq 0) {
    Write-Host "  Modele telecharge avec succes!" -ForegroundColor Green
} else {
    Write-Host "  ERREUR lors du telechargement. Essai avec le modele alternatif..." -ForegroundColor Yellow
    ollama pull avil/UI-TARS
}

# --- ETAPE 5: Verifier que le modele fonctionne ---
Write-Host "`n[5/6] Test du modele..." -ForegroundColor Yellow

$models = ollama list 2>$null
Write-Host "  Modeles disponibles:" -ForegroundColor Cyan
Write-Host $models

# --- ETAPE 6: Instructions pour UI-TARS Desktop ---
Write-Host "`n[6/6] Installation UI-TARS Desktop..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ETAPES MANUELLES REQUISES" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Telecharger UI-TARS Desktop:" -ForegroundColor White
Write-Host "   https://github.com/bytedance/UI-TARS-desktop/releases" -ForegroundColor Blue
Write-Host "   -> Telecharger le fichier .exe (Windows)" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Installer l'application" -ForegroundColor White
Write-Host "   -> Si Windows Defender bloque: 'More info' -> 'Run anyway'" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Configurer le modele local dans UI-TARS Desktop:" -ForegroundColor White
Write-Host "   -> Ouvrir Settings/Parametres" -ForegroundColor Gray
Write-Host "   -> Provider: 'Custom/OpenAI-Compatible'" -ForegroundColor Gray
Write-Host "   -> Base URL: http://localhost:11434/v1" -ForegroundColor Green
Write-Host "   -> API Key: ollama" -ForegroundColor Green
Write-Host "   -> Model: 0000/ui-tars-1.5-7b-q8_0:q8" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ALTERNATIVE: Agent TARS CLI" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Pour utiliser en ligne de commande:" -ForegroundColor White
Write-Host '  $env:OLLAMA_HOST = "http://127.0.0.1:11434"' -ForegroundColor Green
Write-Host '  npx @agent-tars/cli@latest --provider ollama --model "0000/ui-tars-1.5-7b-q8_0:q8"' -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SETUP TERMINE!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Prochaine etape: Lancer UI-TARS Desktop et tester une mission" -ForegroundColor Yellow
