# Agent GUI Autonome - Context pour Claude

## IMPORTANT : Fichier Mission
**Toujours lire `mission.md` en premier** - contient l'état actuel du travail en cours et l'historique des actions.

## Description du Projet

Agent IA autonome qui contrôle un ordinateur Windows via vision (capture d'écran) + actions (souris/clavier).
Tourne 100% en local sur RTX 3090 avec le modèle qwen3-vl:30b via Ollama.

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Capture écran  │────▶│  qwen3-vl:30b   │────▶│  PyAutoGUI      │
│  (PIL)          │     │  (Ollama)       │     │  (Actions)      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Fichiers Principaux

| Fichier | Rôle |
|---------|------|
| `agent_gui.py` | Agent générique avec vision - capture écran, envoie au VLM, exécute actions |
| `smart_agent.py` | Agent avec mémoire persistante - apprend des missions réussies |
| `tiktok_analyzer.py` | Script spécialisé pour analyser les vidéos TikTok |
| `memory.json` | Base de données des missions apprises (JSON) |
| `chrome_utils.py` | Fonctions utilitaires Chrome (ouvrir/fermer onglet, URL) |

## Configuration Technique

- **Modèle VLM**: qwen3-vl:30b (Ollama)
- **API Ollama**: http://localhost:11434/api/generate
- **GPU**: RTX 3090 24GB (~20GB VRAM utilisés)
- **Clavier**: AZERTY français (utilise clipboard pour caractères spéciaux)

## Particularités de qwen3-vl

⚠️ **Important**: qwen3-vl retourne ses réponses dans le champ `thinking`, pas `response`.
Le code doit vérifier les deux champs:
```python
result = data.get("response", "")
thinking = data.get("thinking", "")
if not result.strip() and thinking:
    result = thinking
```

## Actions Supportées

L'agent comprend ces commandes:
- `click at (X, Y)` - cliquer aux coordonnées
- `type "texte"` - taper du texte (via clipboard pour AZERTY)
- `press win/enter/tab/escape` - touches spéciales
- `hotkey ctrl+l` - combinaisons de touches
- `scroll down/up` - défiler
- `wait N` - attendre N secondes
- `DONE` - mission terminée

## Commandes Rapides

```bash
# Agent simple
python agent_gui.py "Ta mission"

# Agent avec mémoire
python smart_agent.py "Ta mission"

# Voir la mémoire
python smart_agent.py --memory

# Analyseur TikTok
python tiktok_analyzer.py
```

## Raccourcis Batch (après ajout au PATH)

```bash
agent "Ta mission"      # agent_gui.py
smart "Ta mission"      # smart_agent.py avec mémoire
tiktok                  # Analyseur TikTok
```

## Dépendances

```
pyautogui>=0.9.54
Pillow>=10.0.0
requests>=2.31.0
pyperclip>=1.8.0
```

## Points d'Attention pour le Développement

1. **Failsafe PyAutoGUI**: Désactivé dans les scripts (`pyautogui.FAILSAFE = False`)
2. **Timeout Ollama**: 180 secondes pour les requêtes avec images
3. **Détection DONE**: Utiliser regex `^ACTION:\s*DONE` avec flag MULTILINE
4. **Focus fenêtre**: Toujours cliquer sur la fenêtre cible avant de taper du texte

## Améliorations Futures Possibles

- [ ] Support multi-écrans
- [ ] Enregistrement vidéo des sessions
- [ ] Interface web pour lancer les missions
- [ ] Plus de modèles VLM supportés
- [ ] Détection d'erreurs et retry automatique
