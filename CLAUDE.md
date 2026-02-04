# Agent GUI Autonome - Context pour Claude

**GitHub**: https://github.com/ctrambouze/agent_computer_use

## IMPORTANT : Fichier Mission
**Toujours lire `mission.md` en premier** - contient l'état actuel du travail en cours.

---

## Stack Technique

| Composant | Technologie | Usage |
|-----------|-------------|-------|
| **OCR** | EasyOCR | Détection texte → coordonnées précises |
| **Détection objets** | YOLO v8 (ultralytics) | Personnes, objets → bbox/coordonnées |
| **VLM** | qwen3-vl:30b (Ollama) | Raisonnement, compréhension d'image |
| **Automatisation** | PyAutoGUI | Souris, clavier, captures |
| **Clipboard** | pyperclip | Copier/coller texte |
| **Images** | Pillow (PIL) | Capture écran, manipulation images |
| **GPU** | RTX 3090 24GB | CUDA pour OCR/YOLO/VLM |

---

## RÈGLE CRITIQUE

⚠️ **Les VLM (qwen3-vl, UI-TARS, etc.) ne donnent PAS de coordonnées pixel précises !**

- Pour cliquer sur du **texte** (menu, bouton) → utiliser **OCR (EasyOCR)**
- Pour cliquer sur un **objet** (personne) → utiliser **YOLO**
- Pour **comprendre/décider** → utiliser **VLM**

---

## Tous les Modules et Fonctions

### ocr_utils.py - Détection de texte (COORDONNÉES PRÉCISES)
```python
from ocr_utils import find_text_on_screen, click_on_text, find_all_text_on_screen

# Trouver un texte → retourne {x, y, confidence, text, bbox}
result = find_text_on_screen("Copier le lien")
if result:
    print(f"Trouvé à ({result['x']}, {result['y']})")

# Trouver et cliquer directement
click_on_text("Enregistrer")

# Lister tous les textes à l'écran
texts = find_all_text_on_screen()
```

### tiktok_copier_lien.py - Copier lien TikTok
```python
from tiktok_copier_lien import copier_lien_tiktok, ouvrir_tiktok_droite

# Ouvre TikTok à droite de l'écran
ouvrir_tiktok_droite()

# Copie le lien via clic droit + OCR
lien = copier_lien_tiktok(video_x=1200, video_y=400)
```

### chrome_utils.py - Contrôle Chrome
```python
from chrome_utils import (
    ouvrir_onglet,      # Ctrl+T
    fermer_onglet,      # Ctrl+W
    ouvrir_url,         # Ouvre une URL
    focus_chrome,       # Met Chrome au premier plan
    is_chrome_running,  # Vérifie si Chrome tourne
    launch_chrome       # Lance Chrome
)
```

### notepad_utils.py - Contrôle Notepad
```python
from notepad_utils import (
    ouvrir_notepad,     # Ouvre Notepad
    ecrire_texte,       # Écrit du texte
    effacer_tout,       # Efface tout
    sauvegarder,        # Sauvegarde (chemin)
    fermer_notepad,     # Ferme Notepad
    nouveau_fichier     # Nouveau fichier
)
```

### explorer_utils.py - Contrôle Explorateur Windows
```python
from explorer_utils import (
    ouvrir_explorateur, # Ouvre l'Explorateur
    ouvrir_dossier,     # Ouvre un dossier
    naviguer_vers,      # Navigue vers un chemin
    remonter_dossier,   # Remonte au parent
    retour,             # Navigation arrière
    avant,              # Navigation avant
    nouveau_dossier,    # Crée un dossier
    rechercher,         # Recherche
    fermer_explorateur  # Ferme
)
```

### window_utils.py - Contrôle Fenêtres
```python
from window_utils import (
    lister_fenetres,    # Liste les fenêtres
    focus_fenetre,      # Focus par process/titre
    minimiser_fenetre,  # Win+Down
    maximiser_fenetre,  # Win+Up
    fermer_fenetre,     # Alt+F4
    minimiser_tout,     # Win+D
    basculer_fenetre,   # Alt+Tab
    fenetre_gauche,     # Win+Left
    fenetre_droite,     # Win+Right
    fermer_application  # Force kill
)
```

### mouse_utils.py - Contrôle Souris
```python
from mouse_utils import (
    position,           # Position actuelle
    deplacer,           # Déplace la souris
    clic,               # Clic gauche
    clic_droit,         # Clic droit
    double_clic,        # Double clic
    triple_clic,        # Triple clic
    drag,               # Glisser-déposer
    scroll_haut,        # Scroll vers le haut
    scroll_bas          # Scroll vers le bas
)
```

### YOLO - Détection d'objets
```python
from ultralytics import YOLO

model = YOLO('yolov8n.pt')  # Nano, rapide
results = model('screenshot.png')

for box in results[0].boxes:
    cls = int(box.cls[0])
    label = model.names[cls]  # 'person', 'car', etc.
    x1, y1, x2, y2 = box.xyxy[0].tolist()
    center_x = int((x1 + x2) / 2)
    center_y = int((y1 + y2) / 2)
    print(f"{label} à ({center_x}, {center_y})")
```

---

## Commandes CLI

```bash
# Copier lien TikTok (TikTok doit être ouvert)
python tiktok_copier_lien.py

# Copier lien TikTok (ouvre TikTok automatiquement)
python tiktok_copier_lien.py --open

# Trouver un texte à l'écran
python ocr_utils.py find "Mon texte"

# Trouver et cliquer sur un texte
python ocr_utils.py click "Enregistrer"

# Lister tous les textes
python ocr_utils.py all

# Agent VLM
python agent_gui.py "Ta mission"
```

---

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

---

## Points d'Attention

1. **Failsafe PyAutoGUI**: Désactivé (`pyautogui.FAILSAFE = False`)
2. **OCR lent au 1er appel**: EasyOCR charge le modèle, rapide ensuite
3. **Focus fenêtre**: Toujours cliquer sur la fenêtre cible avant de taper
4. **Clavier AZERTY**: Utiliser clipboard pour caractères spéciaux
5. **YOLO modèles**: `yolov8n.pt` (rapide), `yolov8n-pose.pt` (pose/keypoints)

---

## Workflow Type

1. **Capturer l'écran** → `ImageGrab.grab()`
2. **Trouver l'élément** :
   - Texte → `ocr_utils.find_text_on_screen()`
   - Objet → YOLO
3. **Agir** → `pyautogui.click(x, y)`
4. **Vérifier** → recapturer et analyser

---

## CE QUI MARCHE vs CE QUI NE MARCHE PAS

### ✅ CE QUI MARCHE
- **OCR sur zone croppée** : crop la zone d'intérêt AVANT l'OCR (ex: TikTok à gauche = crop 0-480)
- **OCR pour texte lisible** : menus, boutons, titres
- **YOLO pour objets** : personnes, objets visuels
- **Clic droit + menu contextuel** : fonctionne bien sur TikTok

### ❌ CE QUI NE MARCHE PAS
- **OCR sur petits chiffres** : likes, comments trop petits → passer en paramètre
- **VLM pour coordonnées** : qwen3-vl invente les positions
- **OCR full screen** : se mélange avec texte des autres fenêtres
- **UI-TARS** : timeout, ne répond pas

### 💡 OPTIMISATIONS
```python
# MAUVAIS - OCR full screen
result = find_text_on_screen("Copier le lien")  # Trouve dans toutes les fenêtres!

# BON - OCR sur zone croppée
screenshot = ImageGrab.grab()
tiktok_zone = screenshot.crop((0, 0, 480, 600))  # Seulement TikTok
tiktok_zone.save('temp.png')
results = reader.readtext('temp.png')
```
