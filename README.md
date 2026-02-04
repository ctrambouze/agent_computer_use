# Agent GUI Autonome - Computer Use

Agent IA autonome qui controle un ordinateur Windows via vision + actions.
Tourne 100% en local sur RTX 3090 avec qwen3-vl:30b.

## Fonctionnalites

- **Vision temps reel** : capture et analyse l'ecran
- **Controle complet** : souris, clavier, navigation
- **Multi-etapes** : execute des missions complexes
- **TikTok Analyzer** : analyse les videos trending

## Stack Technique

| Composant | Technologie |
|-----------|-------------|
| VLM | qwen3-vl:30b via Ollama |
| Vision | PIL ImageGrab |
| Controle | PyAutoGUI + Pyperclip |
| GPU | RTX 3090 24GB |

## Installation

```powershell
# 1. Installer Ollama
winget install Ollama.Ollama

# 2. Telecharger le modele
ollama pull qwen3-vl:30b

# 3. Installer les dependances Python
pip install -r requirements.txt
```

## Utilisation

### Agent Generique

```powershell
cd D:\github\agent_computer_use
python agent_gui.py "Ta mission ici"
```

**Exemples de missions :**
```powershell
# Observation
python agent_gui.py "Decris ce que tu vois sur l'ecran"

# Action simple
python agent_gui.py "Ouvre le menu demarrer"

# Multi-etapes
python agent_gui.py "Ouvre Chrome et va sur google.com"

# Notepad
python agent_gui.py "Ouvre Notepad et ecris: Hello World!"
```

### Analyseur TikTok

Analyse les videos TikTok et sauvegarde les resultats dans Notepad.

```powershell
python tiktok_analyzer.py
```

Resultat :
- Ouvre Chrome sur TikTok
- Analyse 5 videos (titre, likes, commentaires)
- Scroll entre chaque video
- Sauvegarde tout dans Notepad

## Fichiers

| Fichier | Description |
|---------|-------------|
| `agent_gui.py` | Agent generique avec vision |
| `tiktok_analyzer.py` | Analyseur TikTok specialise |
| `launch-agent.ps1` | Lanceur PowerShell |
| `requirements.txt` | Dependances Python |

## Actions Disponibles

L'agent comprend ces commandes :

- `click at (X, Y)` - cliquer aux coordonnees
- `type "texte"` - taper du texte (AZERTY compatible)
- `press win/enter/tab/escape` - touches speciales
- `hotkey ctrl+l` - combinaisons de touches
- `scroll down/up` - defiler
- `wait N` - attendre N secondes
- `DONE` - mission terminee

## Configuration

Le modele utilise par defaut : `qwen3-vl:30b`

Pour changer, modifier dans `agent_gui.py` :
```python
MODEL = "qwen3-vl:30b"  # ou autre modele Ollama avec vision
```

## Notes

- **AZERTY** : le clavier francais est supporte via clipboard (Ctrl+V)
- **Failsafe** : deplacer la souris en coin haut-gauche pour arreter
- **GPU** : necessite ~20GB VRAM pour qwen3-vl:30b

## Auteur

Cree avec Claude Code - Fevrier 2026
