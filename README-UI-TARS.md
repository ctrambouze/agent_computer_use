# Agent Computer Use - UI-TARS + RTX 3090

Agent GUI autonome qui voit l'écran et contrôle l'ordinateur.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Options d'utilisation                     │
├─────────────────┬──────────────────┬────────────────────────────┤
│  UI-TARS Desktop│  Agent TARS CLI  │     Agent Python Custom    │
│  (GUI Electron) │  (Terminal)      │     (PyAutoGUI)            │
└────────┬────────┴────────┬─────────┴─────────────┬──────────────┘
         │                 │                       │
         └────────────────┬┴───────────────────────┘
                          │
              ┌───────────▼───────────┐
              │    Ollama Server      │
              │  localhost:11434      │
              └───────────┬───────────┘
                          │
              ┌───────────▼───────────┐
              │   RTX 3090 (24GB)     │
              │   UI-TARS 1.5 7B Q8   │
              │   ou Qwen3-VL 30B     │
              └───────────────────────┘
```

## Modèles Disponibles

| Modèle | Taille | VRAM | Usage |
|--------|--------|------|-------|
| `0000/ui-tars-1.5-7b-q8_0:q8` | 8.1 GB | ~10 GB | GUI Automation (recommandé) |
| `qwen3-vl:30b` | 19 GB | ~21 GB | Vision générale |
| `avil/UI-TARS` | 3.6 GB | ~5 GB | GUI Automation (léger) |

## Installation Rapide

```powershell
# 1. Setup (une seule fois)
.\setup-ui-tars.ps1

# 2. Installer les deps Python (optionnel, pour agent custom)
pip install -r requirements.txt
```

## Utilisation

### Option 1: UI-TARS Desktop (Recommandé)

1. Télécharger depuis [GitHub Releases](https://github.com/bytedance/UI-TARS-desktop/releases)
2. Installer et lancer
3. Configurer:
   - **Provider**: Custom/OpenAI-Compatible
   - **Base URL**: `http://localhost:11434/v1`
   - **API Key**: `ollama`
   - **Model**: `0000/ui-tars-1.5-7b-q8_0:q8`

### Option 2: Agent TARS CLI

```powershell
# Lancer avec le script
.\launch-agent.ps1 -CLI -Model ui-tars

# Ou directement
$env:OLLAMA_HOST = "http://127.0.0.1:11434"
npx @agent-tars/cli@latest --provider ollama --model "0000/ui-tars-1.5-7b-q8_0:q8"
```

### Option 3: Agent Python Custom

```powershell
# Lancer l'agent
python agent_gui.py "Ouvre Chrome et va sur google.com"

# Ou en interactif
python agent_gui.py
```

## Commandes Utiles

```powershell
# Voir le statut
.\launch-agent.ps1 -Status

# Lister les modèles
ollama list

# Tester un modèle
ollama run 0000/ui-tars-1.5-7b-q8_0:q8

# Voir l'utilisation GPU
nvidia-smi
```

## Missions de Test

### Niveau 1 - Simple
```
Ouvre Chrome, va sur google.com, recherche "test"
```

### Niveau 2 - Moyen
```
Ouvre le bloc-notes, écris "Hello World", sauvegarde sur le bureau sous "test.txt"
```

### Niveau 3 - Avancé (TikTok)
```
Ouvre Chrome, va sur tiktok.com, scroll les 5 premières vidéos trending,
note pour chacune: description visible, nombre de likes approximatif.
Retourne un résumé.
```

## Fichiers

```
D:\github\agent_computer_use\
├── setup-ui-tars.ps1      # Script d'installation
├── launch-agent.ps1       # Script de lancement
├── test-ui-tars.ps1       # Script de test
├── agent_gui.py           # Agent Python custom
├── requirements.txt       # Dépendances Python
└── README-UI-TARS.md      # Cette documentation
```

## Configuration Ollama

```powershell
# Variable d'environnement (définie par setup)
$env:OLLAMA_MODELS = "D:\DATA\ollama\models"

# Redémarrer Ollama après modification
taskkill /F /IM ollama.exe
ollama serve
```

## Troubleshooting

### "Model not found"
```powershell
ollama pull 0000/ui-tars-1.5-7b-q8_0:q8
```

### Ollama ne répond pas
```powershell
# Vérifier si le serveur tourne
curl http://localhost:11434/api/tags

# Redémarrer
taskkill /F /IM ollama.exe
ollama serve
```

### GPU pas utilisé
```powershell
# Vérifier CUDA
nvidia-smi

# Vérifier que OLLAMA_MODELS pointe vers D:
echo $env:OLLAMA_MODELS
```

### UI-TARS Desktop ne se connecte pas
- Vérifier Base URL: `http://localhost:11434/v1` (avec `/v1`)
- API Key: mettre n'importe quoi, ex: `ollama`
- Model: nom exact du modèle Ollama

## Liens

- [UI-TARS GitHub](https://github.com/bytedance/UI-TARS)
- [UI-TARS Desktop](https://github.com/bytedance/UI-TARS-desktop)
- [UI-TARS 1.5 7B Q8 Ollama](https://ollama.com/0000/ui-tars-1.5-7b-q8_0:q8)
- [Ollama](https://ollama.com)
