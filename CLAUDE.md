# Agent GUI Autonome - Context pour Claude

**GitHub**: https://github.com/ctrambouze/agent_computer_use

## IMPORTANT : Fichier Mission
**Toujours lire `mission.md` en premier** - contient l'état actuel du travail en cours et l'historique des actions.

## Description du Projet

Agent IA autonome qui contrôle un ordinateur Windows via vision (capture d'écran) + actions (souris/clavier).
Tourne 100% en local sur RTX 3090.

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Capture écran  │────▶│  Detection      │────▶│  PyAutoGUI      │
│  (PIL)          │     │  (OCR/YOLO/VLM) │     │  (Actions)      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Méthodes de Détection

| Méthode | Usage | Précision Coordonnées |
|---------|-------|----------------------|
| **EasyOCR** | Détection de texte (menus, boutons) | ✅ Excellente |
| **YOLO** | Détection d'objets (personnes, objets) | ✅ Bonne |
| **qwen3-vl** | Compréhension d'image, raisonnement | ❌ Pas de coordonnées précises |

⚠️ **Important**: Les VLM (qwen3-vl, etc.) ne donnent PAS de coordonnées pixel précises. Utiliser OCR ou YOLO pour la localisation.

## Fichiers Principaux

| Fichier | Rôle |
|---------|------|
| `agent_gui.py` | Agent générique avec VLM - capture écran, envoie au VLM, exécute actions |
| `smart_agent.py` | Agent avec mémoire persistante - apprend des missions réussies |
| `tiktok_copier_lien.py` | Copie le lien d'une vidéo TikTok via OCR |
| `ocr_utils.py` | **Fonctions OCR** - détection de texte avec coordonnées (EasyOCR) |
| `chrome_utils.py` | Fonctions Chrome (ouvrir/fermer onglet, URL) |
| `notepad_utils.py` | Fonctions Notepad (ouvrir, écrire, sauvegarder, fermer) |
| `explorer_utils.py` | Fonctions Explorateur (ouvrir dossier, naviguer) |
| `window_utils.py` | Fonctions fenêtres (minimiser, maximiser, fermer, ancrer) |
| `mouse_utils.py` | Fonctions souris (clic, double-clic, drag, scroll) |

## Module OCR (ocr_utils.py)

Utilise **EasyOCR** pour détecter du texte à l'écran avec coordonnées précises.

```python
from ocr_utils import find_text_on_screen, click_on_text

# Trouver un texte et obtenir ses coordonnées
result = find_text_on_screen("Copier le lien")
if result:
    print(f"Trouvé à ({result['x']}, {result['y']})")

# Trouver et cliquer directement
click_on_text("Enregistrer")
```

### Fonctions disponibles:
- `find_text_on_screen(text)` - trouve un texte, retourne {x, y, confidence}
- `find_all_text_on_screen()` - liste tous les textes détectés
- `click_on_text(text)` - trouve et clique sur un texte

## Module YOLO (ultralytics)

Pour la détection d'objets (personnes, etc.).

```python
from ultralytics import YOLO
model = YOLO('yolov8n.pt')
results = model('screenshot.png')
for box in results[0].boxes:
    x1, y1, x2, y2 = box.xyxy[0].tolist()
    center_x = int((x1 + x2) / 2)
    center_y = int((y1 + y2) / 2)
```

## Configuration Technique

- **OCR**: EasyOCR (GPU)
- **Détection objets**: YOLO v8 (ultralytics)
- **VLM** (raisonnement): qwen3-vl:30b (Ollama)
- **API Ollama**: http://localhost:11434/api/generate
- **GPU**: RTX 3090 24GB
- **Clavier**: AZERTY français (utilise clipboard pour caractères spéciaux)

## Commandes Rapides

```bash
# Copier lien TikTok (TikTok doit être ouvert à droite)
python tiktok_copier_lien.py

# Copier lien TikTok (ouvre TikTok automatiquement)
python tiktok_copier_lien.py --open

# Trouver un texte à l'écran
python ocr_utils.py find "Mon texte"

# Trouver et cliquer sur un texte
python ocr_utils.py click "Enregistrer"

# Agent VLM simple
python agent_gui.py "Ta mission"
```

## Dépendances

```
pyautogui>=0.9.54
Pillow>=10.0.0
requests>=2.31.0
pyperclip>=1.8.0
easyocr>=1.7.0
ultralytics>=8.0.0
opencv-python>=4.8.0
```

## Points d'Attention pour le Développement

1. **Failsafe PyAutoGUI**: Désactivé dans les scripts (`pyautogui.FAILSAFE = False`)
2. **OCR vs VLM**: Utiliser OCR pour les coordonnées précises, VLM pour le raisonnement
3. **Initialisation EasyOCR**: Lente au premier appel (charge le modèle), rapide ensuite
4. **Focus fenêtre**: Toujours cliquer sur la fenêtre cible avant de taper du texte
5. **YOLO modèles**: `yolov8n.pt` (nano, rapide), `yolov8n-pose.pt` (détection de pose)

## Workflow Recommandé pour Cliquer sur un Élément

1. **Texte/Menu/Bouton** → Utiliser `ocr_utils.find_text_on_screen()`
2. **Personne/Objet** → Utiliser YOLO
3. **Décision complexe** → Utiliser VLM pour comprendre, puis OCR/YOLO pour agir
